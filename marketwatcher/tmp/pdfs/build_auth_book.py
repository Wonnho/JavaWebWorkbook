from pathlib import Path
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "spring-authentication-beginners-guide.pdf"
WORKFLOW_IMAGE = ROOT / "docs" / "spring-authentication-workflow.png"

PAGE_W, PAGE_H = A4
MARGIN = 44
CONTENT_W = PAGE_W - 2 * MARGIN

NAVY = colors.HexColor("#102A56")
BLUE = colors.HexColor("#246BCE")
TEAL = colors.HexColor("#0B8F87")
GOLD = colors.HexColor("#F4C542")
INK = colors.HexColor("#1C2736")
MUTED = colors.HexColor("#5D6B7D")
LIGHT_BLUE = colors.HexColor("#EAF3FF")
LIGHT_TEAL = colors.HexColor("#EAF8F6")
LIGHT_GOLD = colors.HexColor("#FFF7D8")
PANEL = colors.HexColor("#F5F7FA")
LINE = colors.HexColor("#D8E0EA")
WHITE = colors.white


CODE = {
    "dependencies": """implementation 'org.springframework.boot:spring-boot-starter-web'
implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
implementation 'org.springframework.boot:spring-boot-starter-security'
implementation 'org.springframework.boot:spring-boot-starter-oauth2-client'
implementation 'org.springframework.boot:spring-boot-starter-validation'
implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
runtimeOnly 'org.mariadb.jdbc:mariadb-java-client'""",
    "profiles": """spring.profiles.default=local
spring.config.import=optional:file:.env[.properties]
app.security.remember-me.key=${REMEMBER_ME_KEY}
spring.security.oauth2.client.registration.kakao.client-id=${KAKAO_CLIENT_ID}
spring.security.oauth2.client.registration.kakao.client-secret=${KAKAO_CLIENT_SECRET}""",
    "env": """# .env - local only; never commit
DB_URL=jdbc:mariadb://localhost:3306/webdb
DB_USERNAME=local_user
DB_PASSWORD=change-me
REMEMBER_ME_KEY=long-random-local-value
KAKAO_CLIENT_ID=rest-api-key
KAKAO_CLIENT_SECRET=rotated-secret""",
    "member": """@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member {
    @Id private String mid;
    private String mpw;
    private String email;
    private boolean del;
    private boolean social;
    @ElementCollection private Set<MemberRole> roleSet = new HashSet<>();
}""",
    "join_dto": """@Getter @Setter
public class MemberJoinDTO {
    @NotBlank @Size(min = 4, max = 40)
    private String mid;
    @NotBlank @Size(min = 10, max = 72)
    private String mpw;
    @NotBlank @Email
    private String email;
}""",
    "repo": """public interface MemberRepository
        extends JpaRepository<Member, String> {
    boolean existsById(String mid);
    @EntityGraph(attributePaths = "roleSet")
    Optional<Member> findByMidAndSocialFalse(String mid);
    boolean existsByEmailIgnoreCase(String email);
}""",
    "encoder": """@Configuration
public class PasswordEncoderConfiguration {
    @Bean
    PasswordEncoder passwordEncoder() {
        return PasswordEncoderFactories
                .createDelegatingPasswordEncoder();
    }
}""",
    "join_service": """@Transactional
public void join(MemberJoinDTO dto) throws MidExistException {
    if (memberRepository.existsById(dto.getMid())) {
        throw new MidExistException();
    }
    Member member = Member.localMember(
            dto.getMid(),
            passwordEncoder.encode(dto.getMpw()),
            dto.getEmail());
    member.addRole(MemberRole.USER);
    memberRepository.save(member);
}""",
    "join_controller": """@PostMapping("/join")
public String join(@Valid @ModelAttribute("form") MemberJoinDTO form,
                   BindingResult errors,
                   RedirectAttributes redirect) {
    if (errors.hasErrors()) return "member/join";
    memberService.join(form);
    redirect.addFlashAttribute("result", "joined");
    return "redirect:/member/login";
}""",
    "join_html": """<form th:action="@{/member/join}"
      th:object="${form}" method="post">
  <input th:field="*{mid}" autocomplete="username">
  <p th:errors="*{mid}"></p>
  <input th:field="*{mpw}" type="password"
         autocomplete="new-password">
  <p th:errors="*{mpw}"></p>
  <input th:field="*{email}" type="email">
  <button type="submit">Create account</button>
</form>""",
    "security": """@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(auth -> auth
        .requestMatchers("/css/**", "/js/**", "/member/join",
                         "/member/login", "/oauth2/**", "/login/**")
        .permitAll()
        .requestMatchers("/board/register").authenticated()
        .anyRequest().permitAll());
    http.formLogin(form -> form.loginPage("/member/login"));
    return http.build();
}""",
    "login_html": """<form th:action="@{/member/login}" method="post">
  <input name="username" autocomplete="username">
  <input name="password" type="password"
         autocomplete="current-password">
  <label><input type="checkbox" name="remember-me">
         Keep me signed in</label>
  <button type="submit">Login</button>
</form>""",
    "user_details": """@Override
public UserDetails loadUserByUsername(String mid) {
    Member member = memberRepository.findByMidAndSocialFalse(mid)
        .orElseThrow(() -> new UsernameNotFoundException(mid));
    return new MemberSecurityDTO(
        member.getMid(), member.getMpw(), member.getEmail(),
        member.isDel(), member.isSocial(), toAuthorities(member));
}""",
    "principal": """super(username, password,
      true,              // enabled
      true,              // accountNonExpired
      true,              // credentialsNonExpired
      !del,              // accountNonLocked
      authorities);""",
    "principal_view": """<span sec:authorize="isAuthenticated()">
  Signed in as
  <strong sec:authentication="name"></strong>
</span>
<a sec:authorize="isAnonymous()" th:href="@{/member/login}">
  Login
</a>""",
    "logout": """<form th:action="@{/member/logout}" method="post"
      sec:authorize="isAuthenticated()">
  <button type="submit">Logout</button>
</form>""",
    "remember": """http.rememberMe(remember -> remember
    .key(rememberMeKey)
    .tokenRepository(persistentTokenRepository())
    .userDetailsService(customUserDetailsService)
    .tokenValiditySeconds(60 * 60 * 24 * 30));""",
    "token_repo": """@Bean
PersistentTokenRepository persistentTokenRepository(DataSource dataSource) {
    JdbcTokenRepositoryImpl repository = new JdbcTokenRepositoryImpl();
    repository.setDataSource(dataSource);
    return repository;
}""",
    "token_sql": """CREATE TABLE persistent_logins (
  username  VARCHAR(64) NOT NULL,
  series    VARCHAR(64) PRIMARY KEY,
  token     VARCHAR(64) NOT NULL,
  last_used TIMESTAMP NOT NULL
);""",
    "oauth_props": """spring.security.oauth2.client.registration.kakao.client-id=${KAKAO_CLIENT_ID}
spring.security.oauth2.client.registration.kakao.client-secret=${KAKAO_CLIENT_SECRET}
spring.security.oauth2.client.registration.kakao.authorization-grant-type=authorization_code
spring.security.oauth2.client.registration.kakao.redirect-uri={baseUrl}/login/oauth2/code/{registrationId}
spring.security.oauth2.client.registration.kakao.scope=profile_nickname,account_email
spring.security.oauth2.client.provider.kakao.user-name-attribute=id""",
    "oauth_entry": """<a th:href="@{/oauth2/authorization/kakao}">
  Continue with Kakao
</a>""",
    "oauth_load": """@Override
public OAuth2User loadUser(OAuth2UserRequest request) {
    OAuth2User kakaoUser = super.loadUser(request);
    String provider = request.getClientRegistration()
                             .getRegistrationId();
    String subject = kakaoUser.getName();
    return findOrCreatePrincipal(provider, subject,
                                 kakaoUser.getAttributes());
}""",
    "oauth_identity": """@Entity
@Table(uniqueConstraints = @UniqueConstraint(
    columnNames = {"provider", "providerSubject"}))
public class OAuthIdentity {
    @Id @GeneratedValue private Long id;
    private String provider;
    private String providerSubject;
    @ManyToOne(optional = false) private Member member;
}""",
    "oauth_repo": """public interface OAuthIdentityRepository
        extends JpaRepository<OAuthIdentity, Long> {
    Optional<OAuthIdentity> findByProviderAndProviderSubject(
        String provider, String providerSubject);
}""",
    "oauth_create": """String unusable = passwordEncoder.encode(
        UUID.randomUUID().toString());
Member member = Member.socialMember(
        generatedMid(provider, subject), unusable, email);
member.addRole(MemberRole.USER);
memberRepository.save(member);
identityRepository.save(
        new OAuthIdentity(provider, subject, member));""",
    "oauth_success": """http.oauth2Login(oauth -> oauth
    .loginPage("/member/login")
    .userInfoEndpoint(info -> info
        .userService(customOAuth2UserService))
    .defaultSuccessUrl("/board/list", true));""",
    "mustache": """<form action="/member/join" method="post">
  <input type="hidden" name="{{csrfParameter}}"
         value="{{csrfToken}}">
  <input name="mid" value="{{form.mid}}">
  <input name="mpw" type="password">
  <input name="email" type="email" value="{{form.email}}">
  <button type="submit">Create account</button>
</form>""",
    "csrf_model": """@ControllerAdvice
public class CsrfModelAdvice {
    @ModelAttribute
    void csrf(CsrfToken token, Model model) {
        model.addAttribute("csrfParameter", token.getParameterName());
        model.addAttribute("csrfToken", token.getToken());
    }
}""",
    "signup_test": """mockMvc.perform(post("/member/join")
        .with(csrf())
        .param("mid", "reader01")
        .param("mpw", "LongPassword!23")
        .param("email", "reader@example.com"))
    .andExpect(status().is3xxRedirection())
    .andExpect(redirectedUrl("/member/login"));""",
    "login_test": """mockMvc.perform(formLogin("/member/login")
        .user("reader01")
        .password("LongPassword!23"))
    .andExpect(authenticated().withUsername("reader01"));""",
    "csrf_test": """mockMvc.perform(post("/member/join")
        .param("mid", "attacker"))
    .andExpect(status().isForbidden());""",
    "prod": """server.forward-headers-strategy=framework
server.servlet.session.cookie.secure=true
server.servlet.session.cookie.http-only=true
server.servlet.session.cookie.same-site=lax
spring.jpa.hibernate.ddl-auto=validate
server.error.include-message=never
logging.level.org.springframework.security=INFO""",
}


def L(title, summary, details, code=None, verify="", mistake="", note=""):
    return {
        "title": title,
        "summary": summary,
        "details": details,
        "code": code,
        "verify": verify,
        "mistake": mistake,
        "note": note,
    }


CHAPTERS = [
    ("1", "Think in Requests, Not Pages", [
        L("The browser does not call your service directly", "A browser sends an HTTP request. Spring routes that request through security filters before a controller can run.", ["Start every diagnosis with method, URL, headers, cookies, and body.", "A rendered page is only a convenient request builder; a user can send the same request with Talend, curl, or test code.", "Server-side validation and authorization remain necessary even when the HTML form looks restricted."], verify="Open browser devtools and identify one GET and one POST request.", mistake="Treating a hidden or read-only HTML field as a security control."),
        L("Authentication and authorization are different", "Authentication answers who the caller is. Authorization answers whether that caller may perform this action.", ["A successful password or Kakao login establishes an authenticated principal.", "URL rules and method rules evaluate that principal and its authorities.", "A user can be authenticated but still receive 403 Forbidden when a required role is absent."], verify="Write one protected operation and state the identity and authority it requires.", mistake="Assuming login automatically grants every application permission."),
        L("Sign-up is not login", "Sign-up creates durable member data; login proves credentials and creates authenticated state.", ["The join service writes a member and encoded password.", "The form-login filter later reads that member and checks the submitted password.", "Redirecting to the login page after sign-up makes this boundary visible."], verify="After joining, confirm that the browser is still anonymous until login succeeds.", mistake="Putting an Authentication object into the session from ordinary sign-up code."),
        L("Four stores, four responsibilities", "The browser, HTTP session, member database, and remember-me table store different kinds of state.", ["The browser stores cookies and rendered page data.", "The server session stores security context for the current visit.", "The member table stores identity, password hash, status, and roles.", "The persistent-login table stores revocable remember-me token material."], verify="For each value, name the store that owns it.", mistake="Saying the full Member object is stored inside JSESSIONID."),
        L("Read a 302, 401, 403, 404, and 500", "Status codes reveal which layer rejected or redirected a request.", ["302 commonly means login success redirect or anonymous redirect to login.", "401 means authentication is required or failed in an API-style flow.", "403 often means CSRF or authorization failure.", "404 means no controller or resource matched; 500 means application code failed."], verify="Reproduce a CSRF 403 and a missing-route 404, then compare logs.", mistake="Changing controller code before identifying the status and failing layer."),
        L("Trace before you edit", "A reliable debugging trace follows browser -> filters -> controller -> service -> repository -> database, then the response backward.", ["Mark the last successful step.", "Inspect the input and output of the next method.", "Make one change, rerun the same request, and preserve the evidence."], verify="Draw the trace for POST /member/join in five boxes.", mistake="Changing security, controller, and template simultaneously."),
    ]),
    ("2", "Prepare the Project Boundary", [
        L("Choose the smallest dependency set", "The authentication slice needs web MVC, persistence, security, validation, one view engine, OAuth2 client, and the database driver.", ["Each starter activates auto-configuration and a family of classes.", "Keep Thymeleaf as the main worked engine.", "Add Mustache only when running the Mustache variant, not merely to copy one template."], code="dependencies", verify="Run the dependency report and locate Spring Security and OAuth2 Client.", mistake="Adding JWT or resource-server dependencies to a session-based MVC application."),
        L("Understand package responsibilities", "Package by responsibility so a beginner can predict where code belongs.", ["controller accepts web input and selects a view or redirect.", "service owns use-case rules and transactions.", "repository queries persistent state.", "security adapts members and OAuth2 users into Spring Security principals.", "config composes infrastructure beans and filter behavior."], verify="Locate MemberController, MemberServiceImpl, MemberRepository, and CustomSecurityConfig.", mistake="Putting password encoding or repository calls in the HTML template."),
        L("Use profiles for environment differences", "Shared authentication behavior belongs in application.properties; machine-specific and production-specific values belong in profiles or environment variables.", ["Local configuration may point to localhost and enable helpful SQL logs.", "Production configuration must use injected database settings and conservative error output.", "The same Java code should run in both environments."], code="profiles", verify="Start with the local profile and print only non-secret active-profile information.", mistake="Copying a production secret into application-prod.properties."),
        L("Externalize secrets with .env", "A local .env file can supply developer secrets when it is ignored by Git; cloud deployments should inject environment variables directly.", ["Keep .env.example with names and fake values.", "Rotate any credential that appeared in a screenshot, commit, or log.", "Do not print configuration objects that contain client secrets."], code="env", verify="Use git check-ignore to prove that .env is ignored.", mistake="Believing deletion from the latest commit removes a secret from Git history."),
        L("Prepare MariaDB deliberately", "Authentication depends on stable member and token tables, unique keys, and a least-privilege application account.", ["Use a separate database user for the application.", "Give it only the schema privileges the application needs.", "Use migrations or validated schema in production instead of uncontrolled updates."], verify="Connect as the application user and confirm access only to the intended schema.", mistake="Deploying with the MariaDB root account."),
        L("Create a safe checkpoint", "Before authentication work, the project should compile, start, connect to MariaDB, and render one public page.", ["Record the active profile and Java version.", "Run tests before changing code.", "Commit configuration names but never .env contents."], verify="Produce one clean build and one successful GET /member/login.", mistake="Debugging OAuth2 while the base application cannot start reliably."),
    ]),
    ("3", "Model Members and Input Safely", [
        L("The Member entity is server-owned state", "The entity represents trusted persistent state, not the shape of an incoming form.", ["mid is the local identifier.", "mpw stores an encoded value, never a raw password.", "del, social, and roleSet affect security decisions and must be controlled by the server."], code="member", verify="Inspect the member table and identify each security-sensitive column.", mistake="Binding request parameters directly into Member."),
        L("Use a narrow join DTO", "A request DTO should list only fields the joining user is allowed to supply.", ["Allow mid, mpw, and email.", "Do not expose del, social, or roleSet.", "A malicious extra parameter then has no destination in the input object."], code="join_dto", verify="Send social=true and confirm it cannot change the stored social flag.", mistake="Adding entity fields to the DTO merely because ModelMapper can copy them."),
        L("Validation defines an input contract", "Bean Validation rejects malformed input before business logic attempts persistence.", ["NotBlank handles null, empty, and whitespace-only text.", "Size constrains resource usage and communicates product rules.", "Email checks basic address structure but does not prove ownership."], code="join_dto", verify="Test blank ID, short password, oversized ID, and malformed email.", mistake="Using @Email as proof that the caller owns the address."),
        L("Server defaults defeat mass assignment", "The service or domain factory assigns del=false, social=false, and the USER role regardless of submitted parameters.", ["The controller passes only the validated DTO.", "The domain factory creates a valid local member.", "The service adds the least-privileged starting role."], verify="Inspect the saved row after a direct crafted request.", mistake="Trusting a checkbox named social because the normal page does not display it."),
        L("Roles are authorities with meaning", "MemberRole values become GrantedAuthority values such as ROLE_USER.", ["Persist roles as controlled enum values.", "Map them to authorities when building the principal.", "Do not accept role names from sign-up input."], verify="Login and inspect the authenticated authorities in a debugger or test.", mistake="Letting a user post roleSet=ADMIN."),
        L("Deleted is not enabled", "A soft-deleted member must be represented as disabled or locked when Spring Security builds UserDetails.", ["The database query may exclude deleted rows, or the principal flags may reject them.", "Using both makes the rule explicit.", "A three-argument User constructor defaults all account-state flags to true."], code="principal", verify="Set del=true for a test member and confirm authentication fails.", mistake="Storing del but never connecting it to authentication."),
        L("Local identity and social identity differ", "A local username and a provider subject are different identifiers even if both accounts report the same email.", ["Local login is anchored to mid and password.", "Kakao login is anchored to provider=kakao and Kakao's stable subject id.", "Email is profile data unless the application performs a deliberate verified-linking flow."], verify="Write the unique key for local and Kakao identities separately.", mistake="Auto-linking by matching email alone."),
        L("Design invariants before constructors", "A domain factory can express valid creation paths more clearly than a public all-fields builder.", ["localMember sets social=false and requires an encoded password.", "socialMember sets social=true and receives an unusable encoded placeholder only if the schema requires mpw.", "Neither path accepts deleted state or administrator roles."], verify="List the fields each factory accepts and the fields it owns.", mistake="Using Lombok builder from controller code with every entity field available."),
    ]),
    ("4", "Build Sign-Up End to End", [
        L("GET /member/join prepares the form", "The GET handler creates an empty DTO and returns the member/join view.", ["Use a stable model name such as form.", "The same model name is reused after validation failure.", "GET must not create a member or mutate the database."], verify="Refresh the page repeatedly and confirm the member count does not change.", mistake="Performing registration from a GET request."),
        L("Thymeleaf binds fields explicitly", "th:object and th:field connect the form to the DTO while keeping the HTML readable.", ["The browser ultimately submits ordinary name=value fields.", "type=password prevents visible display but does not encrypt transport.", "HTTPS protects form data in transit in production."], code="join_html", verify="View rendered source and locate names, action, method, and CSRF input.", mistake="Assuming type=password replaces HTTPS or password hashing."),
        L("POST binds, validates, then decides", "The controller handles web concerns: binding errors, redirects, flash messages, and view selection.", ["@Valid triggers DTO constraints.", "BindingResult must immediately follow the validated parameter.", "Invalid input returns the same view; valid input calls the service once."], code="join_controller", verify="Place a breakpoint at memberService.join and prove invalid input never reaches it.", mistake="Redirecting after validation failure and losing field errors."),
        L("The service owns the use case", "MemberServiceImpl enforces uniqueness, encodes the password, assigns safe defaults, and saves in one transaction.", ["The controller does not know how a password is stored.", "The repository does not choose roles.", "A transaction keeps related member and role writes consistent."], code="join_service", verify="Cause a duplicate ID and confirm no partial role data is written.", mistake="Encoding the password in JavaScript or the controller."),
        L("Repository queries state, not policy", "MemberRepository exposes focused persistence questions such as existsById and findByMidAndSocialFalse.", ["A repository method name should reveal the query intent.", "Service code interprets the answer as a business decision.", "Database unique constraints remain the final defense against races."], code="repo", verify="Add a unique constraint and test two attempts with the same mid.", mistake="Relying only on existsById without a database uniqueness rule."),
        L("Use Post-Redirect-Get", "A successful POST returns a redirect so browser refresh does not submit the sign-up form again.", ["The redirect response is commonly 302.", "The browser follows it with GET /member/login.", "Flash attributes survive exactly that redirect journey."], verify="Inspect the 302 Location header, then the following GET.", mistake="Returning the login template directly from POST /member/join."),
        L("Handle duplicate IDs as expected input", "A duplicate ID is a user-correctable outcome, not a server crash.", ["Translate the service exception into a field or form error.", "Keep the non-password fields so the user can correct the ID.", "Do not echo the submitted password back into HTML."], verify="Submit a duplicate and confirm status, message, and preserved safe fields.", mistake="Showing a database stack trace to the browser."),
        L("Never log the join DTO", "A generated toString method includes mpw unless it is explicitly excluded.", ["Remove log.info(memberJoinDTO).", "Log an event identifier and non-sensitive member ID only when necessary.", "Treat logs as production data that operators and systems can read."], verify="Search logs after registration and confirm the raw password never appears.", mistake="Masking only the UI while leaving the password in debug logs."),
        L("Inspect the stored result", "A successful registration should produce one member, one encoded password, and the expected USER role.", ["The stored password begins with an encoder identifier such as {bcrypt} when using a delegating encoder.", "The value differs across encodings because salts are expected.", "Use matches for verification; never compare encoded strings for equality."], verify="Query the member and role tables and count the written rows.", mistake="Expecting two encodings of the same password to be identical."),
        L("Test a request outside the page", "Talend or MockMvc proves the server does not depend on the normal HTML to enforce security.", ["Send only allowed fields and a valid CSRF token.", "Then add del=true, social=true, and roleSet=ADMIN.", "The stored account must still be active, local, and USER only."], code="signup_test", verify="Run the malicious extra-field case and inspect the database.", mistake="Disabling CSRF simply to make an API tool request convenient."),
    ]),
    ("5", "Encode and Verify Passwords", [
        L("Hashing is one-way", "PasswordEncoder transforms a raw password into a salted verifier that is designed not to be decoded.", ["Encryption is reversible with a key; password hashing is intentionally one-way.", "A random salt prevents equal passwords from producing equal stored strings.", "Login supplies the raw candidate again and calls matches."], verify="Encode one password twice and compare the two stored strings and two match results.", mistake="Looking for a decrypt method."),
        L("Create one PasswordEncoder bean", "Configuration constructs the shared encoder; services and security providers inject the PasswordEncoder interface.", ["A single bean gives registration and login compatible behavior.", "DelegatingPasswordEncoder stores an algorithm prefix.", "The prefix supports controlled future migration."], code="encoder", verify="Start the application and confirm there is exactly one intended PasswordEncoder bean.", mistake="Calling new BCryptPasswordEncoder separately with inconsistent policy."),
        L("Encode at the service boundary", "The raw password should exist only long enough to validate and encode the registration or change request.", ["The DTO receives raw input.", "The service calls encode immediately before domain persistence.", "The entity and repository see only the encoded value."], code="join_service", verify="Use a debugger and identify the last method that can see the raw password.", mistake="Saving raw first and planning to encode later."),
        L("Match; do not re-encode", "At login, PasswordEncoder.matches(rawCandidate, storedEncoded) handles salts and algorithm prefixes.", ["Re-encoding creates a new salt and usually a different string.", "Spring Security's DaoAuthenticationProvider performs the match for form login.", "Application controllers should not implement their own login comparison."], verify="Prove that encodedA != encodedB while both match the same raw value.", mistake="Comparing encode(submitted) to the database string."),
        L("Choose password rules deliberately", "Length is the most useful beginner rule; avoid silent truncation and arbitrary complexity that users cannot understand.", ["Set a clear minimum and a database column large enough for encoded values.", "Allow password managers and long passphrases.", "Rate limiting and breached-password checks are deployment additions, not reasons to store weaker hashes."], verify="Test the shortest accepted and longest supported inputs.", mistake="Limiting passwords to a tiny length because the old UI did."),
        L("Change passwords through one service", "A password-change use case validates the new raw value, encodes it, and updates the authenticated member only.", ["Take the member ID from Authentication, not from an editable form field.", "Check the update count or load the entity.", "Revoke remember-me tokens after a sensitive credential change."], verify="Change a password, fail login with the old value, and succeed with the new value.", mistake="Letting the request choose another user's mid."),
        L("Treat hashes as sensitive", "An encoded password is safer than raw text but still valuable to an attacker attempting offline guesses.", ["Do not put hashes into HTML, JSON, logs, or DTOs sent to clients.", "Restrict database and backup access.", "Use a slow adaptive encoder and monitor upgrade needs."], verify="Search rendered pages and logs for {bcrypt} or known hash prefixes.", mistake="Calling a password hash public because it cannot be directly decoded."),
    ]),
    ("6", "Compose the Security Filter Chain", [
        L("Filters run before controllers", "Spring Security can redirect, reject, authenticate, or enrich a request before MVC selects a controller.", ["This explains why a controller breakpoint is never reached for some 403 responses.", "The filter chain is ordered infrastructure, not a controller interceptor list.", "Use security debug logs temporarily and carefully."], verify="Trigger an anonymous protected request and observe the redirect before controller execution.", mistake="Adding controller code to fix a filter-level CSRF failure."),
        L("Write authorization rules explicitly", "A readable allowlist makes public and protected routes visible in one place.", ["Permit login, join, required static assets, and OAuth2 endpoints.", "Require authentication for member changes and protected board actions.", "Give anyRequest a deliberate final policy."], code="security", verify="List every public endpoint needed to complete login and sign-up.", mistake="Leaving authorizeHttpRequests commented out."),
        L("Order request matchers from specific to general", "The first matching authorization rule determines the decision.", ["Specific protected or role-based paths come before broad patterns.", "Static assets should be permitted rather than unnecessarily bypassing all security when possible.", "The final anyRequest rule closes the policy."], verify="Add a test for each matcher category.", mistake="Putting anyRequest().permitAll() before protected matchers."),
        L("Configure a custom login page", "loginPage tells Spring where to send an anonymous browser and which page the application renders.", ["GET /member/login renders the template.", "POST /member/login is processed by Spring Security, not MemberController.", "Input names default to username and password unless configured otherwise."], code="security", verify="Set breakpoints and prove the POST does not call a controller login method.", mistake="Writing a POST login controller that duplicates Spring Security."),
        L("Keep CSRF enabled for browser sessions", "A browser automatically attaches cookies, so a malicious site may cause unwanted state-changing requests unless a CSRF token is required.", ["Thymeleaf integrates with Spring Security to render the token for POST forms.", "API tools must first obtain a session and token or tests must use csrf().", "CSRF is not authentication and does not validate input."], verify="Compare the same POST with and without the correct CSRF token.", mistake="Disabling CSRF globally after seeing one 403."),
        L("Use an access-denied path intentionally", "An authenticated user without permission and a request with invalid CSRF may both result in 403, but logs and handlers should distinguish diagnosis.", ["Keep user-facing output simple.", "Log a correlation ID and safe reason server-side.", "Do not expose stack traces or security internals."], verify="Exercise authenticated role denial and CSRF denial separately.", mistake="Assuming every 403 means the user has the wrong role."),
        L("Prefer configuration injection", "Security keys and collaborators should be injected rather than created inside the filterChain method.", ["Inject PasswordEncoder, user-details service, and remember-me key.", "Use a bean for handlers that need dependencies when practical.", "This improves testability and prevents duplicate configurations."], verify="Count new expressions inside CustomSecurityConfig and justify each one.", mistake="Calling passwordEncoder() manually when constructor injection is available."),
        L("Build a route policy test table", "Turn the authorization design into executable cases for anonymous, USER, and ADMIN callers.", ["For each URL, record method and expected result.", "Include redirects as well as 200, 403, and 404 outcomes.", "Update the table whenever a controller endpoint is added."], verify="Create at least one MockMvc test per row category.", mistake="Testing only the logged-in happy path."),
    ]),
    ("7", "Implement Form Login", [
        L("Render the login form correctly", "The form posts to Spring Security's processing URL with exact credential parameter names.", ["Use type=password for the password field.", "Use autocomplete hints for password managers.", "Show error and logout messages without echoing credentials."], code="login_html", verify="Inspect the outgoing request and confirm username, password, remember-me, and CSRF fields.", mistake="Using type=text for the password input."),
        L("Understand the authentication call chain", "UsernamePasswordAuthenticationFilter creates a token, AuthenticationManager delegates, and DaoAuthenticationProvider loads the member and checks the password.", ["The controller is not part of this credential-check path.", "Each component has one responsibility.", "A failure becomes an authentication failure response, not a repository exception page."], verify="Trace one successful login with security logs or debugger breakpoints.", mistake="Calling MemberRepository from the login page controller."),
        L("Load local members with roles", "CustomUserDetailsService translates a persistent Member into the UserDetails contract Spring Security understands.", ["Query roles in the same authentication read to avoid lazy-loading surprises.", "Exclude or disable social-only records from local password login.", "Throw UsernameNotFoundException without revealing account details to the user."], code="user_details", verify="Load a known member and inspect username, hash, flags, and authorities.", mistake="Returning null when a member is absent."),
        L("Map role enums to authorities", "A stored USER role becomes a SimpleGrantedAuthority named ROLE_USER.", ["hasRole('USER') adds the ROLE_ prefix conceptually.", "hasAuthority('ROLE_USER') compares the full string.", "Choose one naming convention and use it consistently."], verify="Compare hasRole and hasAuthority tests for the same principal.", mistake="Persisting both USER and ROLE_USER inconsistently."),
        L("Represent account status accurately", "UserDetails flags must reflect deletion, lock, expiration, and credential status decisions.", ["For the current model, del should at least prevent authentication.", "Do not use the convenient constructor when its enabled defaults are wrong.", "Status policy belongs in one translation layer."], code="principal", verify="Run a login test with del=true.", mistake="Assuming the presence of a del column automatically affects Spring Security."),
        L("Let PasswordEncoder perform verification", "DaoAuthenticationProvider calls matches using the submitted raw password and stored encoded password.", ["The database value should keep its {id} prefix for a delegating encoder.", "A missing or malformed prefix causes an encoder error unless migration is configured.", "Registration and authentication must use compatible encoders."], verify="Register a new member and immediately authenticate through the real form flow.", mistake="Removing {bcrypt} from the stored value for appearance."),
        L("Handle login failure without account discovery", "The page may say credentials are invalid without revealing whether the username exists.", ["Use a common message for absent member and wrong password.", "Preserve no password value.", "Add rate limiting or monitoring at deployment time."], verify="Compare browser messages for unknown user and wrong password.", mistake="Showing 'this username exists but the password is wrong'."),
        L("Use the principal in MVC safely", "Controllers may inject @AuthenticationPrincipal or use Principal when they need the authenticated member ID.", ["Do not accept an editable writer or member ID as the authority source.", "Use principal.getUsername() for ownership checks.", "Reload mutable profile state when the operation needs current database truth."], verify="Attempt to update another member by changing a request parameter.", mistake="Trusting a hidden username field over Authentication."),
        L("Render authenticated navigation", "Thymeleaf Security extras can show login, logout, and username elements according to the current Authentication.", ["This improves user experience but does not enforce authorization.", "The server security rules still protect endpoints.", "Avoid displaying sensitive principal fields."], code="principal_view", verify="Compare navigation as anonymous and authenticated users.", mistake="Using sec:authorize as the only protection for a controller."),
    ]),
    ("8", "Understand HttpSession and Cookies", [
        L("What successful login creates", "After authentication, Spring stores a SecurityContext containing Authentication and associates it with the current request and session strategy.", ["The principal represents the signed-in user.", "Authorities support later authorization decisions.", "Credentials are commonly erased after authentication."], verify="Inspect Authentication fields after login without logging secrets.", mistake="Expecting the session to contain the raw submitted password."),
        L("What JSESSIONID contains", "JSESSIONID is normally an opaque identifier that lets the server locate session state; it is not the serialized Member object.", ["The browser returns it automatically for matching requests.", "Anyone who steals a valid session ID may act as that session until it expires or is invalidated.", "Protect it with HTTPS and cookie flags."], verify="Compare the cookie value with server-side session attributes.", mistake="Decoding JSESSIONID to look for the username."),
        L("Follow the cookie round trip", "The server sends Set-Cookie after creating a session, and the browser sends Cookie on later requests.", ["Cookie scope depends on domain, path, SameSite, Secure, and expiry attributes.", "A session cookie usually has no long absolute lifetime.", "Browser devtools show both the response and later request."], verify="Capture the Set-Cookie response and next Cookie request.", mistake="Looking only at the HTML body when debugging session behavior."),
        L("Session state stays server-side", "The session may live in application memory or an external store, while the browser holds only its identifier.", ["A server restart can remove in-memory sessions.", "Multiple cloud instances need sticky routing or a shared session store.", "The book's core implementation begins with one server instance."], verify="Restart locally and observe whether the login session survives.", mistake="Assuming sessions automatically work across every cloud topology."),
        L("Session fixation protection", "Spring Security changes or migrates the session identifier at authentication so an attacker cannot preselect the authenticated session ID.", ["Observe the identifier before and after login.", "Do not disable the default strategy without a specific reason.", "Session fixation protection complements HTTPS and CSRF."], verify="Record JSESSIONID before login and after successful login.", mistake="Reusing a caller-supplied session ID unchanged after authentication."),
        L("Session timeout is not remember-me", "A session timeout removes active server-side state; remember-me can later create a new authenticated context using a separate token.", ["Without remember-me, the user signs in again.", "With valid remember-me, a returning request can be authenticated automatically.", "Sensitive actions may require full recent authentication."], verify="Test session expiry once with and once without remember-me.", mistake="Setting a 30-day session and calling it remember-me."),
        L("Cookie flags have distinct jobs", "HttpOnly limits script access, Secure limits HTTPS transport, and SameSite influences cross-site sending.", ["HttpOnly does not stop the browser from sending the cookie.", "Secure requires HTTPS and may affect local testing.", "SameSite=Lax is a common MVC starting point but must be tested with OAuth2 redirects."], verify="Inspect all flags in production-like HTTPS.", mistake="Thinking HttpOnly prevents CSRF."),
        L("Read session data through security APIs", "Application code normally reads Authentication rather than manually parsing session attributes or cookies.", ["Spring Security maintains the context lifecycle.", "Manual cookie parsing bypasses validation and coupling rules.", "Use SecurityContextHolder only where method injection is unsuitable."], verify="Replace any direct JSESSIONID parsing with principal or Authentication access.", mistake="Using the cookie value as a user ID."),
        L("Scale sessions intentionally", "Cloud deployment must decide where session state lives and how instances share it.", ["A single instance can use servlet memory initially.", "A multi-instance deployment may use Spring Session with Redis or database storage.", "The decision changes infrastructure, not the sign-up DTO or password encoder."], verify="Document the deployment's instance count and session store.", mistake="Introducing JWT solely because more than one instance might exist."),
        L("Diagnose a lost login", "When login appears to vanish, check redirect host, cookie domain/path, Secure behavior, session restart, and load-balancer routing.", ["Confirm the login response sets a cookie.", "Confirm the next request sends it.", "Confirm the server can resolve that session and security context."], verify="Use a three-column trace: response cookie, request cookie, server session.", mistake="Changing password logic when the browser simply dropped the cookie."),
    ]),
    ("9", "Logout and CSRF", [
        L("Logout is a state-changing POST", "A logout request invalidates authenticated state and should not be triggerable by a passive link or embedded image.", ["Use a form with method=post.", "Let Spring Security's logout filter process it.", "Redirect to a clear logged-out page or login page."], code="logout", verify="Inspect the request method and CSRF field.", mistake="Using a GET hyperlink for logout."),
        L("Place logout in shared navigation", "Most applications need a logout action wherever authenticated navigation appears, not a separate logout.html page.", ["The layout can conditionally render the form for authenticated users.", "A separate confirmation page is optional product behavior.", "Endpoint protection remains in the filter chain."], code="logout", verify="Open two authenticated pages and confirm both expose the same logout action.", mistake="Duplicating slightly different logout forms across templates."),
        L("CSRF protects cookie-authenticated writes", "Because browsers attach session cookies automatically, a token proves the state-changing request came from a page that received the application's token.", ["The token is bound to server-managed request context.", "An attacker site can often send a form but cannot read the valid token due to same-origin protections.", "XSS can defeat CSRF, so output escaping still matters."], verify="Submit the same logout POST with and without a valid token.", mistake="Describing CSRF as password verification."),
        L("Why Talend received 403", "A direct POST without the matching session cookie and CSRF token fails before the controller runs.", ["First GET the form to establish session context and obtain the token.", "Return the same JSESSIONID and token on POST.", "Use application/x-www-form-urlencoded for an MVC form handler unless it expects JSON."], verify="Reproduce both failing and successful Talend requests.", mistake="Sending JSON text to a form-binding controller with application/json."),
        L("What logout should clear", "Logout invalidates the current session, clears the security context, and should remove related remember-me state when configured.", ["The browser may retain an expired cookie entry briefly in devtools.", "The old session ID must no longer authorize requests.", "Other devices require separate session management if global logout is desired."], verify="Replay the old cookie after logout and expect anonymous behavior.", mistake="Judging logout solely by whether the cookie row is visible in devtools."),
        L("Design post-logout feedback", "A redirect such as /member/login?logout communicates success without rendering from the POST request.", ["The login template conditionally shows a small message.", "Do not expose session identifiers or internal reasons.", "Refresh should remain a safe GET."], verify="Logout, refresh, and use Back; protected content must remain inaccessible.", mistake="Returning a cached protected page as proof the session is still valid."),
        L("Test CSRF rather than disabling it", "MockMvc can add a valid token with csrf(), making intended requests concise while preserving negative tests.", ["One test proves missing token is rejected.", "One proves a valid token reaches validation or service logic.", "Keep browser-session CSRF enabled in production configuration."], code="csrf_test", verify="Run both positive and negative POST tests.", mistake="Adding csrf.disable() only to make tests pass."),
    ]),
    ("10", "Add Persistent Remember-Me", [
        L("Remember-me starts after the session", "Persistent remember-me allows a recognized browser to regain Authentication when no valid session security context exists.", ["It is not the same cookie as JSESSIONID.", "It should be optional and clearly labeled.", "A remembered authentication may be considered weaker for sensitive actions."], verify="Delete only JSESSIONID and observe the next request with remember-me retained.", mistake="Calling the remember-me cookie a 30-day session ID."),
        L("Configure one stable key", "The remember-me key signs or protects token processing and must be stable across restarts and secret in production.", ["Load it from app.security.remember-me.key.", "All application instances need the same active value.", "Rotation invalidates existing remember-me cookies, which can be acceptable during incident response."], code="remember", verify="Restart with the same key, then with a different key, and compare behavior.", mistake="Hard-coding a short key in source control."),
        L("Use a persistent token repository", "JdbcTokenRepositoryImpl stores token series and rotating token values so server-side revocation is possible.", ["Inject the application DataSource.", "Create the schema deliberately rather than enabling automatic table creation in production.", "Protect the table like authentication data."], code="token_repo", verify="Select rows after remember-me login and after logout.", mistake="Calling setCreateTableOnStartup(true) in every environment."),
        L("Understand the persistent_logins schema", "A series identifies the remembered login record while token changes as it is used.", ["username links token ownership to a user-details lookup.", "last_used supports rotation and cleanup decisions.", "Token theft detection depends on correct series/token handling."], code="token_sql", verify="Observe how token and last_used change across remembered requests.", mistake="Displaying token values in an administrator page or log."),
        L("The checkbox controls issuance", "Spring Security looks for the remember-me request parameter during a successful interactive login.", ["No checked parameter means no long-lived remember-me cookie.", "The login page should explain the shared-device risk.", "Do not pre-check it silently."], code="login_html", verify="Compare response cookies with the checkbox off and on.", mistake="Issuing remember-me for every user without consent."),
        L("Returning through remember-me", "When JSESSIONID is absent, RememberMeAuthenticationFilter validates the remember-me cookie and loads current user details.", ["Deleted or locked accounts must still be rejected by current status rules.", "Roles are reloaded rather than trusted forever from the browser.", "A new session may then be created for subsequent requests."], verify="Disable a remembered member and confirm automatic login no longer grants access.", mistake="Embedding permanent roles directly in an unrevocable cookie."),
        L("Logout and password changes revoke trust", "A normal logout should clear the cookie and persistent token; password change should revoke remembered devices according to policy.", ["Delete all token rows for that username after sensitive credential changes.", "Provide device management only if product scope requires it.", "Record revocation as a safe security event."], verify="Change the password and attempt to reuse an old remember-me cookie.", mistake="Leaving remembered devices active forever after account compromise."),
        L("Protect the remember-me cookie", "Use HttpOnly, Secure in HTTPS, appropriate SameSite, and the smallest practical scope.", ["The token is a bearer credential.", "Long lifetime increases theft impact.", "TLS and XSS prevention remain essential."], verify="Inspect the production Set-Cookie attributes.", mistake="Assuming a database-backed token is safe if the cookie is exposed."),
        L("Test the two-cookie timeline", "A useful integration test separates interactive login, session removal, remembered recovery, token rotation, and logout.", ["Record JSESSIONID and remember-me after login.", "Remove JSESSIONID only and request a protected page.", "Then logout and prove neither old credential grants access."], verify="Document each request and cookie state in a five-row table.", mistake="Testing remember-me without ever removing the session cookie."),
    ]),
    ("11", "Add Kakao OAuth2 Login", [
        L("OAuth2 login delegates credential checking", "Your application never receives the Kakao password; Kakao authenticates the user and returns authorization results through a standard flow.", ["The application is an OAuth2 client.", "Kakao is the authorization server and user-info provider.", "Your application still creates its own local session after successful login."], verify="Explain which system sees the Kakao password.", mistake="Storing a Kakao password in the member table."),
        L("Start at the authorization endpoint", "The login page links to /oauth2/authorization/kakao, which Spring Security turns into an authorization redirect.", ["The registration ID kakao selects configuration.", "Spring generates state and tracks the authorization request.", "The browser leaves localhost and visits Kakao."], code="oauth_entry", verify="Inspect the 302 Location URL without publishing client secrets.", mistake="Linking the button directly to a guessed Kakao callback URL."),
        L("Consent happens at Kakao", "Kakao shows requested scopes and the user approves according to app and account settings.", ["Request only profile data the application uses.", "account_email may be missing or unavailable.", "A successful Kakao login must not depend blindly on email presence."], verify="Test an account where email consent is unavailable or denied.", mistake="Casting kakao_account.email without null handling."),
        L("The callback carries a code", "Kakao redirects the browser to /login/oauth2/code/kakao with an authorization code and state, not a finished application login.", ["Spring verifies the stored authorization request and state.", "The client exchanges the short-lived code at the token endpoint.", "The configured redirect URI must exactly match Kakao's allowed URI."], verify="Compare the actual callback URI with the Kakao console entry character by character.", mistake="Using /member/login as the OAuth2 callback."),
        L("Understand redirect-uri placeholders", "{baseUrl} becomes the current application origin and {registrationId} becomes kakao.", ["Locally the result is usually http://localhost:8080/login/oauth2/code/kakao.", "In production it uses the public HTTPS origin when forwarded headers are correct.", "A proxy misconfiguration can produce the wrong scheme or host."], code="oauth_props", verify="Print the authorization request redirect URI in local and production-like environments.", mistake="Hard-coding localhost for cloud deployment."),
        L("Exchange the code for tokens", "Spring's OAuth2 client sends the code, client ID, client secret when required, and redirect URI to Kakao's token endpoint.", ["invalid_client or KOE010 points to client credentials or client-authentication configuration.", "Do not log access tokens or client secrets.", "Rotate any secret shown in a screenshot."], verify="Classify an invalid_client error before changing callback code.", mistake="Debugging CustomOAuth2UserService when token exchange never succeeded."),
        L("Fetch the Kakao user", "After token exchange, DefaultOAuth2UserService calls Kakao's user-info endpoint and returns attributes.", ["The configured user-name-attribute=id makes OAuth2User.getName return the stable Kakao subject.", "Nested kakao_account data is optional and must be read defensively.", "Keep raw attributes only as long as needed."], verify="Inspect attribute keys with sensitive values redacted.", mistake="Using nickname as a unique account identifier."),
        L("Customize loadUser after the provider succeeds", "CustomOAuth2UserService should call super.loadUser first, then translate provider identity into an application principal.", ["Read registrationId rather than display clientName for provider keys.", "Use OAuth2User.getName for the provider subject.", "Find or create the local identity in a transaction."], code="oauth_load", verify="Log only provider and a safe correlation identifier during first login.", mistake="Selecting the switch branch by a fragile display label."),
        L("Create the application session", "After the OAuth2 user service returns a valid principal, Spring creates Authentication and applies the session strategy just as it does for form login.", ["The resulting protected-request experience can be the same.", "No Kakao password is placed in the session.", "A success URL sends the browser into the application."], code="oauth_success", verify="Inspect Authentication type and authorities after Kakao login.", mistake="Manually creating JSESSIONID in the OAuth2 service."),
        L("Diagnose ?error in the right layer", "A redirect to /member/login?error says the OAuth2 process failed, but the root cause is in server logs or an OAuth2 failure handler.", ["Separate authorization denial, state mismatch, token exchange, user-info, database, and principal-construction failures.", "Capture exception class and safe error code.", "Fix the earliest failing stage."], verify="Build a table of failure stage, evidence, and likely configuration.", mistake="Assuming every ?error means the Kakao password was wrong."),
        L("Keep OAuth2 secrets and URLs deployable", "Client ID may be public in protocol terms, but client secret and tokens are confidential; all environment-specific values must be externalized.", ["Use a rotated secret in production.", "Register both local and production redirect URIs only where needed.", "Require HTTPS for public callbacks."], code="oauth_props", verify="Search Git history and logs for known secret fragments.", mistake="Committing a regenerated secret because the old one was removed."),
    ]),
    ("12", "Create Social Members Safely", [
        L("Replace the 1111 block", "The current shared-password member creation should be replaced inside the empty-result branch, not followed by a second creation block.", ["A shared 1111 becomes a local credential if local login can reach the record.", "It also couples onboarding state to a password comparison.", "Use provider identity and explicit profile state instead."], verify="Search the project for raw and encoded comparisons with 1111.", mistake="Adding secure creation below the old memberRepository.save call."),
        L("Key identity by provider and subject", "The durable social key is the pair kakao plus Kakao's stable id.", ["Email can change, be absent, or collide with a local account.", "A unique database constraint prevents duplicate provider identities.", "The provider subject should not be editable profile data."], code="oauth_identity", verify="Attempt to insert the same provider and subject twice.", mistake="Using email as the only social-login lookup."),
        L("Add an OAuth identity repository", "The repository answers one question: which local member owns this provider subject?", ["Load the related member and roles efficiently for login.", "Keep provider-specific lookup separate from local username lookup.", "Return Optional and handle first versus returning login explicitly."], code="oauth_repo", verify="Test found and absent identities.", mistake="Falling back silently to findByEmail when identity is absent."),
        L("Create exactly one member on first login", "Within a transaction, check the provider identity, create a local member if absent, then persist the unique identity link.", ["Handle concurrent first-login attempts with a unique constraint.", "Generate an internal mid that cannot collide with ordinary input.", "Assign USER and safe server-owned defaults."], code="oauth_create", verify="Run two near-simultaneous first-login attempts and count resulting identities.", mistake="Saving the member without saving a durable provider link."),
        L("Use an unusable random password only for schema compatibility", "If mpw is non-null, store an encoded random value that no person knows and do not enable local password login for that social member.", ["The random value is not the Kakao password.", "Do not return its raw form in MemberSecurityDTO.", "Long term, model credentials according to supported login methods."], code="oauth_create", verify="Confirm local form login cannot select a social-only record.", mistake="Displaying a generated password to the social user without an account-linking design."),
        L("Make onboarding state explicit", "If first-time social users must complete a profile, add a profileCompleted field or a dedicated onboarding record.", ["The success handler reads explicit state.", "Password content no longer controls navigation.", "Completing onboarding updates that state transactionally."], verify="Test new social user and returning completed user redirects.", mistake="Using passwordEncoder.matches('1111', hash) as a profile flag."),
        L("Set OAuth attributes for every principal", "Both new and returning OAuth2 principals must expose a non-null attribute map expected by OAuth2User.", ["Set props after both branches or build the principal in one shared method.", "Do not persist entire provider responses without purpose.", "Avoid putting access tokens in principal attributes."], verify="Call getAttributes for new and returning users.", mistake="Setting props only in the new-member branch."),
        L("Design account linking as a separate secure flow", "Linking a local account to Kakao should require the local authenticated user and a fresh successful Kakao authorization.", ["Verify both sides in the same controlled flow.", "Prevent a matching email from automatically taking ownership.", "Record and allow removal of linked providers with reauthentication."], verify="Write preconditions for link and unlink operations.", mistake="Treating matching email text as proof of common ownership."),
    ]),
    ("13", "Adapt Thymeleaf to Mustache", [
        L("Keep authentication below the view", "Changing template engines should not rewrite MemberService, repositories, PasswordEncoder, SecurityFilterChain, session handling, or OAuth2 login.", ["Both engines render HTML forms.", "Both browsers send the same HTTP request.", "The difference is expression syntax and integration helpers."], verify="Draw a boundary around files that change when switching engines.", mistake="Creating a Mustache-specific authentication service."),
        L("Translate form binding", "Thymeleaf uses th:object, th:field, and th:errors; Mustache uses named inputs and model values or sections.", ["Keep input names identical to DTO property names.", "Repopulate safe fields after validation.", "Never repopulate a password field."], code="mustache", verify="Compare the HTTP body produced by both forms.", mistake="Changing controller parameter names during template migration."),
        L("Expose CSRF explicitly when needed", "If Mustache does not automatically render Spring Security's token, a controller advice can expose parameter name and token to the model.", ["Use the actual CsrfToken rather than inventing a hidden value.", "Return it in every state-changing form.", "Test rendered HTML and the resulting POST."], code="csrf_model", verify="View source and compare hidden token name with Spring's expected parameter.", mistake="Hard-coding _csrf and a static token."),
        L("Adapt authentication-aware navigation", "Thymeleaf Security extras provide sec:authorize; Mustache can receive small view-model booleans and display names.", ["View flags improve rendering only.", "SecurityFilterChain still enforces server authorization.", "Expose the minimum principal information needed for the page."], verify="Request the page as anonymous and authenticated in both engines.", mistake="Sending the full MemberSecurityDTO to the template."),
        L("Choose one engine per runnable edition", "A beginner project is clearer when one view resolver and template suffix are active at a time.", ["Keep the complete Thymeleaf edition as the baseline.", "Provide a small Mustache patch or branch.", "Run the same web and security tests against both editions."], verify="Build each edition from a clean checkout.", mistake="Mixing .html and .mustache examples without explaining which resolver renders them."),
    ]),
    ("14", "Test and Diagnose the Whole Mechanism", [
        L("Test sign-up state, not only redirect", "A 302 can hide incorrect stored data, so verify the member, encoded password, role, and server-owned flags.", ["Use a valid CSRF token in the positive request.", "Load the member from the repository.", "Assert passwordEncoder.matches and raw password inequality."], code="signup_test", verify="Add assertions for social=false, del=false, and USER only.", mistake="Declaring success because the browser reached /member/login."),
        L("Test form authentication", "Spring Security test support can submit the real form-login parameters and assert authenticated or unauthenticated results.", ["Seed a member with an encoded password.", "Test correct, wrong, deleted, and social-only cases.", "Assert authorities as well as username."], code="login_test", verify="Run the suite with the same PasswordEncoder bean used by production code.", mistake="Saving a raw password in test fixtures."),
        L("Test malicious direct requests", "Security tests must send requests the normal page never creates.", ["Add del, social, and role parameters to sign-up.", "Change an ownership identifier during an update.", "Remove CSRF and replay old session or remember-me cookies."], code="csrf_test", verify="Confirm each attack fails for the intended reason.", mistake="Testing only browser-generated happy paths."),
        L("Test OAuth2 without calling Kakao", "Mock an OAuth2 user or client exchange so application tests control provider, subject, and attributes.", ["Test first login creates one identity.", "Test returning login reuses it.", "Test absent email and matching local email without takeover."], verify="Assert the unique provider-subject link and local member count.", mistake="Making every test depend on the live Kakao service."),
        L("Use an evidence-first failure checklist", "For any failure, record request, status, redirect, response cookie, server exception, and database effect before editing.", ["Connection refused means the server is not listening.", "404 means mapping or resource resolution.", "403 suggests CSRF or authorization.", "OAuth2 ?error requires the earliest provider/client/database failure."], verify="Complete the checklist for one intentionally broken configuration.", mistake="Applying multiple speculative fixes and losing the original cause."),
    ]),
    ("15", "Prepare for Cloud Deployment", [
        L("Use production cookie and proxy settings", "Public HTTPS and reverse proxies must produce secure cookies and the correct external base URL for redirects.", ["Honor forwarded headers only from trusted infrastructure.", "Set Secure, HttpOnly, and a tested SameSite policy.", "Verify the generated Kakao redirect uses https and the public host."], code="prod", verify="Inspect production-like Set-Cookie and OAuth2 authorization redirects.", mistake="Testing only direct localhost HTTP behavior."),
        L("Deploy secrets and schema safely", "Cloud configuration injects database credentials, remember-me key, and Kakao secret; schema changes are migrated before application startup.", ["Do not upload .env as a public artifact.", "Use a least-privilege database account and backups.", "Set ddl-auto=validate after applying migrations."], code="prod", verify="Run a secret scan and a migration/validate startup in staging.", mistake="Using ddl-auto=update as the production migration plan."),
        L("Final release checklist", "A release is ready when local sign-up, form login, session renewal, logout, remember-me, Kakao login, hostile requests, and recovery behavior are all verified.", ["Remove TRACE security logging and stack traces from user responses.", "Rotate credentials exposed during development.", "Record session-store, token-revocation, backup, and incident-response ownership.", "Ship the smallest system that satisfies the product, then extend from tested boundaries."], verify="Sign the checklist with a build identifier and staging evidence.", mistake="Calling the feature complete after one successful browser login."),
    ]),
]


def ascii_safe(text):
    return (text.replace("\u2013", "-")
                .replace("\u2014", "-")
                .replace("\u2011", "-")
                .replace("\u2018", "'")
                .replace("\u2019", "'")
                .replace("\u201c", '"')
                .replace("\u201d", '"'))


def draw_wrapped(c, text, x, y, width, font="Helvetica", size=9.4,
                 leading=12.2, color=INK, max_lines=None):
    c.setFont(font, size)
    c.setFillColor(color)
    words = ascii_safe(text).split()
    lines = []
    line = ""
    for word in words:
        candidate = word if not line else line + " " + word
        if stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    if max_lines:
        lines = lines[:max_lines]
    for item in lines:
        c.drawString(x, y, item)
        y -= leading
    return y


def draw_bullet(c, text, x, y, width, size=9.1):
    c.setFillColor(TEAL)
    c.circle(x + 3, y + 3, 2, stroke=0, fill=1)
    return draw_wrapped(c, text, x + 13, y + 7, width - 13,
                        size=size, leading=11.7, color=INK)


def draw_code(c, code, x, y, width):
    lines = ascii_safe(code).splitlines()
    line_h = 9.4
    height = 18 + line_h * len(lines)
    c.setFillColor(colors.HexColor("#122033"))
    c.roundRect(x, y - height, width, height, 7, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#D9E8FF"))
    c.setFont("Courier", 6.9 if max((len(a) for a in lines), default=0) > 72 else 7.3)
    yy = y - 14
    for line in lines:
        c.drawString(x + 10, yy, line[:100])
        yy -= line_h
    return y - height - 8


def header(c, chapter, chapter_title, page_num):
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 30, PAGE_W, 30, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN, PAGE_H - 19, f"CHAPTER {chapter}  |  {ascii_safe(chapter_title).upper()}")
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 19, "BUILD SIGN-UP AND LOGIN YOU CAN ADAPT")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 20, str(page_num))


def render_lesson(c, chapter, chapter_title, lesson, page_num, lesson_index):
    header(c, chapter, chapter_title, page_num)
    c.bookmarkPage(f"p{page_num}")
    if lesson_index == 0:
        c.addOutlineEntry(f"Chapter {chapter}: {chapter_title}", f"p{page_num}", level=0)

    y = PAGE_H - 61
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN, y, f"LESSON {chapter}.{lesson_index + 1}")
    y -= 25
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 19)
    title = ascii_safe(lesson["title"])
    if stringWidth(title, "Helvetica-Bold", 19) > CONTENT_W:
        c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, y, title)
    y -= 18
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.line(MARGIN, y, MARGIN + 72, y)
    y -= 18

    # Summary card
    c.setFillColor(LIGHT_BLUE)
    c.roundRect(MARGIN, y - 52, CONTENT_W, 52, 8, stroke=0, fill=1)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN + 12, y - 15, "CORE IDEA")
    draw_wrapped(c, lesson["summary"], MARGIN + 12, y - 31,
                 CONTENT_W - 24, size=9.2, leading=11.5, max_lines=2)
    y -= 72

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "Follow the mechanism")
    y -= 18
    for detail in lesson["details"]:
        y = draw_bullet(c, detail, MARGIN, y, CONTENT_W)
        y -= 6

    if lesson.get("code"):
        y -= 3
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(MARGIN, y, "Project code")
        y -= 10
        y = draw_code(c, CODE[lesson["code"]], MARGIN, y, CONTENT_W)

    # Bottom checkpoint panel uses a stable location to keep pages consistent.
    panel_h = 94 if lesson.get("note") else 78
    panel_y = 42
    c.setFillColor(LIGHT_TEAL)
    c.roundRect(MARGIN, panel_y, CONTENT_W, panel_h, 8, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN + 12, panel_y + panel_h - 17, "CHECKPOINT")
    draw_wrapped(c, lesson.get("verify") or "Explain this step in your own words and verify it in the running project.",
                 MARGIN + 12, panel_y + panel_h - 32, CONTENT_W - 24,
                 size=8.5, leading=10.5, max_lines=2)
    c.setFillColor(colors.HexColor("#A63D40"))
    c.setFont("Helvetica-Bold", 8.3)
    c.drawString(MARGIN + 12, panel_y + 20, "COMMON MISTAKE")
    draw_wrapped(c, lesson.get("mistake") or "Changing several layers before identifying the failing request stage.",
                 MARGIN + 104, panel_y + 20, CONTENT_W - 116,
                 size=8.2, leading=10, color=INK, max_lines=2)


def front_header(c, title, page_num=None):
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 12, PAGE_W, 12, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 21)
    c.drawString(MARGIN, PAGE_H - 63, ascii_safe(title))
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.line(MARGIN, PAGE_H - 77, MARGIN + 82, PAGE_H - 77)
    if page_num:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawCentredString(PAGE_W / 2, 20, str(page_num))


def front_page_1(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 27, PAGE_W, 27, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(52, PAGE_H - 155, "BUILD SIGN-UP AND LOGIN")
    c.drawString(52, PAGE_H - 193, "YOU CAN ADAPT")
    c.setFillColor(colors.HexColor("#9EDFD8"))
    c.setFont("Helvetica-Bold", 15)
    c.drawString(53, PAGE_H - 231, "A beginner's project guide")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 11)
    subtitle = "Spring Boot 3 | Spring Security 6 | HttpSession | Cookies | Remember-Me | Kakao OAuth2"
    draw_wrapped(c, subtitle, 53, PAGE_H - 270, PAGE_W - 106, size=11, leading=15, color=WHITE)

    # Simple three-lane cover motif.
    y = 370
    lanes = [("SIGN UP", LIGHT_BLUE, BLUE), ("FORM LOGIN", LIGHT_TEAL, TEAL), ("KAKAO LOGIN", LIGHT_GOLD, colors.HexColor("#9A6D00"))]
    for label, fill, accent in lanes:
        c.setFillColor(fill)
        c.roundRect(53, y, PAGE_W - 106, 54, 10, stroke=0, fill=1)
        c.setFillColor(accent)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y + 21, label)
        c.line(180, y + 27, PAGE_W - 90, y + 27)
        y -= 72
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 9)
    c.drawString(53, 55, "Project edition for marketwatcher | 120 pages")


def front_page_2(c, page_num):
    front_header(c, "How to use this book", page_num)
    y = PAGE_H - 112
    paragraphs = [
        "This is a build-along book, not a catalog of Spring annotations. Each chapter follows one browser request through filters, controllers, services, repositories, database state, sessions, and cookies.",
        "Use the marketwatcher project as the running application. Complete each checkpoint before moving forward. A chapter ends in a runnable state so a failure can be located without guessing across unfinished layers.",
        "Thymeleaf is the complete implementation. Chapter 13 translates the view-specific pieces to Mustache. The authentication mechanism stays in Spring Security and application services, so the engine swap should not duplicate business logic.",
    ]
    for p in paragraphs:
        y = draw_wrapped(c, p, MARGIN, y, CONTENT_W, size=10.5, leading=15)
        y -= 18
    c.setFillColor(LIGHT_GOLD)
    c.roundRect(MARGIN, y - 150, CONTENT_W, 150, 10, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN + 16, y - 25, "The three questions on every page")
    questions = ["What HTTP request is being handled?", "Which class owns the decision?", "What state changes in the database, session, or browser?"]
    yy = y - 53
    for i, q in enumerate(questions, 1):
        c.setFillColor(BLUE)
        c.circle(MARGIN + 26, yy + 3, 10, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(MARGIN + 26, yy, str(i))
        c.setFillColor(INK)
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 45, yy, q)
        yy -= 34


def front_page_3(c, page_num):
    front_header(c, "What this book builds - and what it does not", page_num)
    y = PAGE_H - 112
    sections = [
        ("Included in the core", LIGHT_TEAL, ["Validated local sign-up and encoded passwords", "Spring Security form login", "HttpSession and JSESSIONID", "CSRF-safe logout", "Persistent remember-me", "Kakao OAuth2 login", "Thymeleaf with a focused Mustache adaptation", "Tests and production-ready configuration boundaries"]),
        ("Deliberately left for a later volume", PANEL, ["JWT APIs and mobile clients", "SAML, MFA, and multi-tenant authorization", "Complete password-reset email delivery", "A full account-management product", "Microservice identity architecture"]),
    ]
    for heading, fill, items in sections:
        h = 48 + len(items) * 24
        c.setFillColor(fill)
        c.roundRect(MARGIN, y - h, CONTENT_W, h, 10, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGIN + 15, y - 24, heading)
        yy = y - 51
        for item in items:
            yy = draw_bullet(c, item, MARGIN + 15, yy, CONTENT_W - 30, size=9.3) - 4
        y -= h + 22


def front_page_4(c, page_num):
    front_header(c, "The complete authentication workflow", page_num)
    if WORKFLOW_IMAGE.exists():
        img = ImageReader(str(WORKFLOW_IMAGE))
        iw, ih = img.getSize()
        max_w = CONTENT_W
        max_h = 420
        scale = min(max_w / iw, max_h / ih)
        w, h = iw * scale, ih * scale
        c.drawImage(img, MARGIN + (CONTENT_W - w) / 2, PAGE_H - 120 - h, width=w, height=h, preserveAspectRatio=True, mask='auto')
        y = PAGE_H - 138 - h
    else:
        y = PAGE_H - 180
        c.setFillColor(PANEL)
        c.rect(MARGIN, y, CONTENT_W, 120, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Read the picture from left to right")
    y -= 22
    points = [
        "Sign-up stores a member; it does not authenticate the browser.",
        "Form login and Kakao login both produce Authentication and then a server-side session.",
        "The browser returns JSESSIONID; persistent remember-me is optional and separate.",
        "Protected requests are authorized from the current Authentication, not from editable form fields.",
    ]
    for p in points:
        y = draw_bullet(c, p, MARGIN, y, CONTENT_W) - 5


def front_page_5(c, page_num):
    front_header(c, "The project architecture", page_num)
    layers = [
        ("VIEW", "join.html | login.html | shared navigation", LIGHT_BLUE),
        ("WEB + FILTERS", "MemberController | Spring Security filters", LIGHT_TEAL),
        ("APPLICATION", "MemberServiceImpl | UserDetailsService | OAuth2UserService", LIGHT_GOLD),
        ("PERSISTENCE", "MemberRepository | OAuthIdentityRepository | token repository", colors.HexColor("#F3EEFF")),
        ("STATE", "MariaDB | HttpSession | browser cookies", PANEL),
    ]
    y = PAGE_H - 128
    for idx, (name, desc, fill) in enumerate(layers):
        c.setFillColor(fill)
        c.roundRect(MARGIN, y - 67, CONTENT_W, 58, 8, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN + 15, y - 31, name)
        c.setFillColor(INK)
        c.setFont("Helvetica", 9.2)
        c.drawString(MARGIN + 132, y - 31, desc)
        if idx < len(layers) - 1:
            c.setStrokeColor(TEAL)
            c.setLineWidth(2)
            c.line(PAGE_W / 2, y - 70, PAGE_W / 2, y - 86)
        y -= 83
    y -= 5
    draw_wrapped(c, "A clean boundary makes adaptation possible: templates change presentation; security and business rules stay in their owning layers.", MARGIN, y, CONTENT_W, size=10, leading=14)


def front_page_6(c, page_num):
    front_header(c, "The recommended learning path", page_num)
    stages = [
        ("1", "Build safe member creation", "DTO -> validation -> service -> password encoder -> repository"),
        ("2", "Add local authentication", "filter chain -> user details -> password match -> Authentication"),
        ("3", "Observe state", "HttpSession -> JSESSIONID -> protected request -> logout"),
        ("4", "Extend persistence", "remember-me cookie -> persistent token -> automatic return"),
        ("5", "Add Kakao", "authorization -> callback -> user info -> provider identity -> session"),
        ("6", "Adapt and deploy", "Mustache view -> hostile tests -> HTTPS -> cloud secrets"),
    ]
    y = PAGE_H - 122
    for number, title, desc in stages:
        c.setFillColor(BLUE)
        c.circle(MARGIN + 18, y - 6, 15, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(MARGIN + 18, y - 10, number)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN + 48, y, title)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + 48, y - 18, desc)
        if number != "6":
            c.setStrokeColor(LINE)
            c.line(MARGIN + 18, y - 24, MARGIN + 18, y - 58)
        y -= 77


def front_page_7(c, page_num):
    front_header(c, "Core vocabulary", page_num)
    terms = [
        ("Principal", "The identity represented by an Authentication."),
        ("Authentication", "The current identity, authorities, and authentication state."),
        ("Authorization", "The decision that an authenticated or anonymous caller may perform an action."),
        ("HttpSession", "Server-side state associated with one browser session identifier."),
        ("JSESSIONID", "An opaque browser cookie commonly used to locate the server session."),
        ("CSRF", "A cross-site request attack that abuses automatically attached browser credentials."),
        ("Remember-me", "A separate long-lived credential that can restore Authentication after the session is gone."),
        ("OAuth2 subject", "A stable user identifier issued by a provider for the client context."),
        ("Password hash", "A salted one-way verifier used by PasswordEncoder.matches."),
    ]
    y = PAGE_H - 112
    for term, meaning in terms:
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(MARGIN, y, term)
        c.setFillColor(INK)
        y = draw_wrapped(c, meaning, MARGIN + 116, y, CONTENT_W - 116, size=9.2, leading=11.5)
        c.setStrokeColor(LINE)
        c.line(MARGIN, y - 5, PAGE_W - MARGIN, y - 5)
        y -= 22


def front_page_8(c, page_num):
    front_header(c, "Contents", page_num)
    y = PAGE_H - 108
    start_page = 9
    for chapter, title, lessons in CHAPTERS:
        c.setFillColor(BLUE if int(chapter) % 2 else TEAL)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(MARGIN, y, f"{chapter.zfill(2)}")
        c.setFillColor(NAVY)
        c.drawString(MARGIN + 32, y, title)
        c.setStrokeColor(LINE)
        c.line(MARGIN + 225, y + 2, PAGE_W - MARGIN - 28, y + 2)
        c.setFillColor(MUTED)
        c.drawRightString(PAGE_W - MARGIN, y, str(start_page))
        y -= 31
        start_page += len(lessons)
    c.setFillColor(LIGHT_GOLD)
    c.roundRect(MARGIN, 55, CONTENT_W, 55, 8, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica", 8.8)
    c.drawString(MARGIN + 12, 86, "Every chapter ends in a runnable checkpoint.")
    c.drawString(MARGIN + 12, 70, "Code blocks show the secure target design for this project, not secret values.")


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("Build Sign-Up and Login You Can Adapt")
    c.setAuthor("marketwatcher project guide")
    c.setSubject("Spring Boot sessions, cookies, form login, remember-me, and Kakao OAuth2")

    front_functions = [front_page_1, front_page_2, front_page_3, front_page_4,
                       front_page_5, front_page_6, front_page_7, front_page_8]
    page_num = 1
    for func in front_functions:
        if func is front_page_1:
            func(c)
        else:
            func(c, page_num)
        c.showPage()
        page_num += 1

    for chapter, chapter_title, lessons in CHAPTERS:
        for idx, lesson in enumerate(lessons):
            render_lesson(c, chapter, chapter_title, lesson, page_num, idx)
            c.showPage()
            page_num += 1

    c.save()

    reader = PdfReader(str(OUTPUT))
    expected = 120
    actual = len(reader.pages)
    if actual != expected:
        raise RuntimeError(f"Expected {expected} pages, generated {actual}")
    if OUTPUT.stat().st_size < 250_000:
        raise RuntimeError("PDF is unexpectedly small")
    print(f"Created {OUTPUT}")
    print(f"Pages: {actual}")
    print(f"Bytes: {OUTPUT.stat().st_size}")


if __name__ == "__main__":
    build()
