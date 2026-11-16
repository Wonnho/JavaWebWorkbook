from pathlib import Path
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from build_auth_book import (  # noqa: E402
    PAGE_W, PAGE_H, MARGIN, CONTENT_W,
    NAVY, BLUE, TEAL, GOLD, INK, MUTED, LIGHT_BLUE, LIGHT_TEAL,
    LIGHT_GOLD, PANEL, LINE, WHITE,
    ascii_safe, draw_wrapped, draw_bullet, draw_code,
)


OUTPUT = ROOT / "output" / "pdf" / "thymeleaf-mustache-frontend-companion.pdf"
BACKEND_PDF = ROOT / "output" / "pdf" / "spring-authentication-beginners-guide.pdf"
IMAGE_DIR = ROOT / "docs" / "frontend-guide-images"


CODES = {
    "thymeleaf_dep": """implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
implementation 'org.thymeleaf.extras:thymeleaf-extras-springsecurity6'
implementation 'nz.net.ultraq.thymeleaf:thymeleaf-layout-dialect:3.1.0'""",
    "mustache_dep": """implementation 'org.springframework.boot:spring-boot-starter-mustache'

# Choose this for the Mustache edition.
# Keep controllers and services unchanged.""",
    "html_root": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org"
      xmlns:sec="http://www.thymeleaf.org/thymeleaf-extras-springsecurity6"
      xmlns:layout="http://www.ultraq.net.nz/thymeleaf/layout">
<head>...</head>
<body>...</body>
</html>""",
    "resource_urls": """<link rel="stylesheet" th:href="@{/css/styles.css}">
<script th:src="@{/js/scripts.js}"></script>
<a th:href="@{/member/login}">Login</a>
<img th:src="@{/assets/favicon.ico}" alt="">""",
    "layout": """<!-- layout/basic.html -->
<main class="container-fluid" layout:fragment="content">
  <p>Default content</p>
</main>
<th:block layout:fragment="script"></th:block>""",
    "child_layout": """<html layout:decorate="~{layout/basic.html}">
<main layout:fragment="content">
  <h1>Create account</h1>
</main>
<script layout:fragment="script" th:inline="javascript">
  // page-specific behavior
</script>
</html>""",
    "fragment": """<!-- fragments/auth-nav.html -->
<nav th:fragment="authNav">
  <a sec:authorize="isAnonymous()" th:href="@{/member/login}">Login</a>
  <span sec:authorize="isAuthenticated()"
        sec:authentication="name"></span>
</nav>

<div th:replace="~{fragments/auth-nav :: authNav}"></div>""",
    "model_get": """@GetMapping("/join")
public String joinGet(Model model) {
    if (!model.containsAttribute("form")) {
        model.addAttribute("form", new MemberJoinDTO());
    }
    return "member/join";
}""",
    "model_attr": """<h1 th:text="${pageTitle}">Fallback title</h1>
<p th:if="${message}" th:text="${message}"></p>
<span th:text="${form.mid}">sample-user</span>""",
    "mustache_vars": """<h1>{{pageTitle}}</h1>
{{#message}}<p>{{message}}</p>{{/message}}
{{^message}}<p>No message</p>{{/message}}
<span>{{form.mid}}</span>""",
    "join_th": """<form th:action="@{/member/join}"
      th:object="${form}" method="post" novalidate>
  <label for="mid">User ID</label>
  <input id="mid" th:field="*{mid}" autocomplete="username">
  <p class="field-error" th:errors="*{mid}"></p>

  <label for="mpw">Password</label>
  <input id="mpw" th:field="*{mpw}" type="password"
         autocomplete="new-password">
  <button type="submit">Create account</button>
</form>""",
    "join_mustache": """<form action="/member/join" method="post" novalidate>
  <input type="hidden" name="{{csrfParameter}}" value="{{csrfToken}}">
  <label for="mid">User ID</label>
  <input id="mid" name="mid" value="{{form.mid}}" autocomplete="username">
  {{#midError}}<p class="field-error">{{midError}}</p>{{/midError}}
  <label for="mpw">Password</label>
  <input id="mpw" name="mpw" type="password" autocomplete="new-password">
  <button type="submit">Create account</button>
</form>""",
    "join_post": """@PostMapping("/join")
public String joinPost(
        @Valid @ModelAttribute("form") MemberJoinDTO form,
        BindingResult errors,
        RedirectAttributes redirect) {
    if (errors.hasErrors()) return "member/join";
    memberService.join(form);
    redirect.addFlashAttribute("result", "joined");
    return "redirect:/member/login";
}""",
    "field_state": """<input th:field="*{email}" type="email"
       th:classappend="${#fields.hasErrors('email')} ? 'is-invalid'">
<p class="field-error" th:if="${#fields.hasErrors('email')}"
   th:errors="*{email}"></p>""",
    "global_errors": """<div class="alert alert-danger"
     th:if="${#fields.hasGlobalErrors()}" role="alert">
  <p th:each="error : ${#fields.globalErrors()}"
     th:text="${error}"></p>
</div>""",
    "flash": """<div class="alert alert-success"
     th:if="${result == 'joined'}" role="status">
  Account created. Sign in below.
</div>""",
    "login_th": """<form th:action="@{/member/login}" method="post">
  <label for="username">User ID</label>
  <input id="username" name="username" autocomplete="username" required>
  <label for="password">Password</label>
  <input id="password" name="password" type="password"
         autocomplete="current-password" required>
  <label><input type="checkbox" name="remember-me"> Keep me signed in</label>
  <button type="submit">Login</button>
</form>""",
    "login_mustache": """<form action="/member/login" method="post">
  <input type="hidden" name="{{csrfParameter}}" value="{{csrfToken}}">
  <label for="username">User ID</label>
  <input id="username" name="username" autocomplete="username">
  <label for="password">Password</label>
  <input id="password" name="password" type="password"
         autocomplete="current-password">
  <button type="submit">Login</button>
</form>""",
    "login_messages": """<div th:if="${param.error}" class="alert alert-danger" role="alert">
  Sign-in failed. Check your credentials and try again.
</div>
<div th:if="${param.logout}" class="alert alert-success" role="status">
  You are signed out.
</div>""",
    "social_link": """<a class="btn btn-warning"
   th:href="@{/oauth2/authorization/kakao}">
  Continue with Kakao
</a>""",
    "auth_nav": """<li sec:authorize="isAnonymous()">
  <a th:href="@{/member/login}">Login</a>
</li>
<li sec:authorize="isAuthenticated()">
  Hello, <span sec:authentication="name"></span>
</li>""",
    "logout_th": """<form th:action="@{/logout}" method="post"
      sec:authorize="isAuthenticated()">
  <button type="submit" class="btn btn-link">Logout</button>
</form>""",
    "logout_mustache": """{{#authenticated}}
<form action="/logout" method="post">
  <input type="hidden" name="{{csrfParameter}}" value="{{csrfToken}}">
  <button type="submit">Logout</button>
</form>
{{/authenticated}}""",
    "csrf_meta": """<meta name="_csrf" th:content="${_csrf.token}">
<meta name="_csrf_header" th:content="${_csrf.headerName}">
<script th:src="@{/js/security.js}" defer></script>""",
    "csrf_js": """const token = document.querySelector('meta[name="_csrf"]')?.content;
const header = document.querySelector('meta[name="_csrf_header"]')?.content;
if (window.axios && token && header) {
  axios.defaults.headers.common[header] = token;
}

// Keep HTML <script> tags out of .js files.""",
    "fetch_csrf": """await fetch('/api/profile', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    [csrfHeader]: csrfToken
  },
  body: JSON.stringify(payload)
});""",
    "common_model": """@ControllerAdvice
public class CommonViewModel {
  @ModelAttribute
  void common(Authentication authentication, CsrfToken csrf, Model model) {
    model.addAttribute("authenticated", authentication != null);
    model.addAttribute("csrfParameter", csrf.getParameterName());
    model.addAttribute("csrfToken", csrf.getToken());
  }
}""",
    "password_toggle": """const button = document.querySelector('[data-password-toggle]');
button?.addEventListener('click', () => {
  const input = document.querySelector('#password');
  const showing = input.type === 'text';
  input.type = showing ? 'password' : 'text';
  button.setAttribute('aria-pressed', String(!showing));
});""",
    "auth_css": """.auth-shell { min-height: 100vh; display: grid; place-items: center; padding: 1rem; }
.auth-card { width: min(100%, 28rem); padding: 1.5rem; border: 1px solid #d8e0ea; }
.field-error { color: #b42318; margin-top: .35rem; }
input:focus-visible, button:focus-visible, a:focus-visible {
  outline: 3px solid #246bce; outline-offset: 2px;
}""",
    "aria": """<label for="email">Email</label>
<input id="email" name="email" type="email"
       autocomplete="email" required
       aria-describedby="email-help email-error"
       aria-invalid="true">
<small id="email-help">We use this for account notices.</small>
<p id="email-error" class="field-error">Enter a valid email.</p>""",
    "mockmvc_view": """mockMvc.perform(get("/member/join"))
  .andExpect(status().isOk())
  .andExpect(view().name("member/join"))
  .andExpect(model().attributeExists("form"))
  .andExpect(content().string(containsString("name=\"mid\"")));""",
    "mockmvc_error": """mockMvc.perform(post("/member/join")
    .with(csrf())
    .param("mid", "")
    .param("mpw", "short")
    .param("email", "bad"))
  .andExpect(status().isOk())
  .andExpect(view().name("member/join"))
  .andExpect(model().attributeHasFieldErrors("form", "mid", "mpw", "email"));""",
}


def L(title, summary, details, connection, code=None, verify="", mistake="", ref=None, image=None):
    return {
        "title": title,
        "summary": summary,
        "details": details,
        "connection": connection,
        "code": code,
        "verify": verify,
        "mistake": mistake,
        "ref": ref,
        "image": image,
    }


REF = {
    1: "Backend Ch. 1, pp. 9-14; Ch. 8, pp. 63-72 - requests, sessions, and browser state",
    2: "Backend Ch. 2, pp. 15-20; Ch. 13, pp. 108-112 - project boundary and template adaptation",
    3: "Backend Ch. 6, pp. 46-53; Ch. 13, pp. 108-112 - route policy and shared views",
    4: "Backend Ch. 4, pp. 29-38; Ch. 7, pp. 54-62 - controller model and authenticated principal",
    5: "Backend Ch. 3, pp. 21-28; Ch. 4, pp. 29-38 - safe DTO and sign-up use case",
    6: "Backend Ch. 3, pp. 21-28; Ch. 4, pp. 29-38 - validation contract and sign-up response",
    7: "Backend Ch. 6, pp. 46-53; Ch. 7, pp. 54-62; Ch. 8, pp. 63-72 - login and session",
    8: "Backend Ch. 8, pp. 63-72; Ch. 9, pp. 73-79; Ch. 10, pp. 80-88 - cookies, logout, CSRF, remember-me",
    9: "Backend Ch. 11, pp. 89-99; Ch. 12, pp. 100-107 - Kakao OAuth2 and social identity",
    10: "Backend Ch. 1, pp. 9-14; Ch. 13, pp. 108-112 - request meaning and template adaptation",
    11: "Backend Ch. 13, pp. 108-112 - translating Thymeleaf to Mustache",
    12: "Backend Ch. 14, pp. 113-117; Ch. 15, pp. 118-120 - tests, diagnostics, and deployment",
}


CHAPTERS = [
    (1, "Follow Data from Browser to Template", [
        L("A page begins as an HTTP request", "Before Thymeleaf or Mustache runs, the browser asks for a URL and Spring Security evaluates the request.", ["Record method, URL, query parameters, cookies, and expected status.", "A GET normally requests representation; a POST normally submits a state-changing form.", "The view engine is near the end of the server response path, not the beginning."], "Browser GET -> SecurityFilterChain -> controller -> model -> template -> HTML.", verify="Inspect GET /member/join in browser devtools.", mistake="Saying the template receives a browser request directly."),
        L("Security can stop the request first", "Security filters may redirect or reject before MemberController is selected.", ["Anonymous access rules decide whether the page is reachable.", "CSRF affects state-changing requests, not ordinary page GETs.", "A controller breakpoint that never runs is evidence to inspect the filter result."], "SecurityFilterChain owns access; the template only controls displayed markup.", verify="Request a protected page anonymously and inspect the redirect.", mistake="Editing join.html to fix a filter-level 403."),
        L("The controller selects data and view", "A controller method adds model attributes and returns a logical template name or redirect.", ["The model is a server-side map for one rendering.", "Returning member/join asks the view resolver to render the matching template.", "Returning redirect:/... creates a redirect response instead of rendering HTML."], "MemberController -> Model -> member/join template.", code="model_get", verify="Break at joinGet and inspect model keys.", mistake="Putting database queries into template expressions."),
        L("The model is a rendering contract", "Templates should receive small, intentional values such as form, errors, message, and authentication display data.", ["A form DTO is safer than exposing a JPA entity.", "A model attribute exists only for rendering unless placed in session scope.", "Name attributes consistently across GET and failed POST."], "model.addAttribute('form', dto) -> th:object or {{form...}}.", code="model_attr", verify="List every model key used by join.html.", mistake="Exposing Member.mpw or a full security principal to the view."),
        L("The engine produces ordinary HTML", "Thymeleaf and Mustache execute on the server and send plain HTML to the browser.", ["The browser never sees th:if, th:field, or Mustache sections after rendering.", "View source reveals the real action, names, hidden CSRF value, and links.", "JavaScript operates on rendered HTML, not server-side template expressions."], "Template syntax -> rendered HTML -> browser DOM.", verify="Compare template source with browser View Source.", mistake="Expecting th:if to run again in the browser."),
        L("The browser builds the POST", "Form controls with a name contribute name=value pairs when the form is submitted.", ["Disabled controls are not submitted.", "Labels, placeholders, and CSS classes do not become request values.", "The form action and method determine the next HTTP request."], "input name='mid' -> request parameter mid -> DTO binding.", verify="Submit join and inspect Form Data.", mistake="Using only id without name and expecting Spring binding."),
        L("Validation chooses view or redirect", "A failed form returns the template with errors; a successful form calls the service and redirects.", ["BindingResult describes field and global errors.", "Returning the view preserves model and safe entered values.", "Post/Redirect/Get prevents refresh from resubmitting a successful POST."], "BindingResult -> error display; MemberService success -> redirect.", verify="Compare network traces for invalid and valid submissions.", mistake="Redirecting on validation error and losing errors."),
        L("Read the full frontend loop", "The final browser GET after a redirect begins a new request and a new rendering cycle.", ["Flash attributes can cross one redirect.", "Session authentication can cross many requests through JSESSIONID.", "Ordinary model attributes do not automatically survive."], "POST -> 302 Location -> browser GET -> new model -> new HTML.", image="frontend-data-flow.png", verify="Trace all twelve boxes using one successful sign-up.", mistake="Treating redirect as an internal method call."),
    ]),
    (2, "Choose Thymeleaf or Mustache", [
        L("Both engines solve the same view problem", "They combine server model data with HTML templates and produce a response body.", ["Thymeleaf uses attributes such as th:text and th:field.", "Mustache uses variables, sections, and inverted sections.", "The HTTP request and backend use case can remain identical."], "Same Model -> chosen renderer -> same browser-facing contract.", image="thymeleaf-mustache-one-backend.png", verify="Explain which layers do not change when engines switch.", mistake="Creating a second MemberService for Mustache."),
        L("Install the Thymeleaf edition", "The current project uses Thymeleaf, Security extras, and a layout dialect.", ["The starter registers a view resolver for templates.", "Security extras provides sec:authorize and sec:authentication.", "The layout dialect supports layout:decorate and fragments."], "Gradle dependencies -> auto-configuration -> template resolver.", code="thymeleaf_dep", verify="Confirm member/login resolves from templates/member/login.html.", mistake="Adding multiple versions of the same dialect."),
        L("Install the Mustache edition", "The alternative edition replaces the view starter while keeping Spring MVC and Security.", ["Mustache templates normally use a .mustache suffix.", "Model keys remain the data source.", "Features such as CSRF and authentication-aware navigation need explicit model values."], "Gradle Mustache starter -> Mustache view resolver -> same controller names.", code="mustache_dep", verify="Render a minimal member/login.mustache.", mistake="Running two view resolvers without understanding precedence."),
        L("Understand natural templates", "Thymeleaf attributes coexist with normal HTML, so a file can retain useful fallback content.", ["th:text replaces element text at render time.", "th:href and th:src produce context-aware URLs.", "Fallback text helps static preview but is not application data."], "HTML fallback -> Thymeleaf replacement -> final HTML.", code="model_attr", verify="Open the template directly and through Spring.", mistake="Assuming fallback sample values are submitted production values."),
        L("Understand Mustache escaping", "Double braces render escaped text, which is the safe default for untrusted content.", ["Sections render when a value is present or truthy.", "Inverted sections render when a value is absent or false.", "Triple braces render unescaped HTML and should be exceptional."], "Model value -> HTML escaping -> response text.", code="mustache_vars", verify="Render text containing <script> and confirm it is escaped.", mistake="Using triple braces for user-authored content."),
        L("Keep view names stable", "Controllers can return member/join in both editions while the active resolver chooses .html or .mustache.", ["Do not put extensions in controller return values.", "Keep URL paths independent from template file extensions.", "Use one complete runnable engine edition at a time."], "Controller logical name -> active view resolver -> physical template.", verify="Swap engine dependency without changing controller return strings.", mistake="Returning member/join.html from controller code."),
        L("Compare syntax, not architecture", "A useful migration compares one function at a time: variables, conditions, loops, forms, errors, CSRF, and principal display.", ["Keep field names and request URLs unchanged.", "Keep validation messages semantically identical.", "Run the same web tests against each edition."], "View syntax changes at the edge; application behavior remains fixed.", verify="Create a two-column syntax checklist.", mistake="Redesigning routes during a template migration."),
        L("Choose the edition for the reader", "Beginners should finish one engine path before translating to the other.", ["This companion teaches Thymeleaf first because it is active in marketwatcher.", "Chapter 11 gives a complete Mustache conversion path.", "Backend cross-references apply to both."], "Thymeleaf baseline -> working feature -> Mustache translation.", verify="State which edition is currently active before editing.", mistake="Mixing snippets from both engines in one file."),
    ]),
    (3, "Build Layouts, Navigation, and Assets", [
        L("Use one html root", "A document should have one html element containing head and body.", ["Declare Thymeleaf, Security extras, and layout namespaces on that root.", "Set lang for assistive technology and search engines.", "Avoid the current duplicate <html> opening tags in basic.html."], "HTML document root -> template namespaces -> valid rendered document.", code="html_root", verify="Validate rendered HTML structure.", mistake="Writing two adjacent html start tags."),
        L("Create a layout content slot", "The shared layout owns chrome; each page supplies its main content fragment.", ["Keep navigation, common CSS, and shared scripts in the layout.", "Use a semantic main region for changing content.", "Default content helps diagnose missing fragments."], "layout:fragment='content' -> replaced by child page fragment.", code="layout", verify="Render join.html and locate its content inside the layout.", mistake="Copying the whole navbar into every page."),
        L("Decorate a child page", "A child declares the base layout and provides matching fragments.", ["The logical relationship is server-side composition.", "Page-specific scripts belong in the script fragment.", "Avoid duplicate head and body markup that conflicts with the layout."], "Child layout:decorate -> base layout -> merged response.", code="child_layout", verify="Inspect final DOM for one head and one body.", mistake="Loading the same script in layout and child."),
        L("Extract reusable fragments", "Small repeated UI such as authentication navigation can be a named fragment.", ["Give the fragment one responsibility.", "Pass explicit parameters when a fragment needs data.", "Keep endpoint protection in SecurityFilterChain even when a link is hidden."], "th:replace -> fragment function -> rendered navigation.", code="fragment", verify="Render the same auth fragment on board and member pages.", mistake="Treating fragment visibility as authorization."),
        L("Generate context-aware URLs", "Thymeleaf @{...} respects the application context path and safely builds query parameters.", ["Use it for links, actions, scripts, images, and stylesheets.", "Mustache normally receives a base path or uses known root-relative routes.", "Test behind the deployment path if the app is not hosted at root."], "@{/path} -> resolved URL -> browser request.", code="resource_urls", verify="Run with a non-root context path.", mistake="Hard-coding localhost:8080 in templates."),
        L("Load static assets once", "CSS belongs in the document head; scripts should be deferred or placed after content according to behavior.", ["Spring Boot serves common static locations.", "The security policy must permit required assets.", "Cache-busted production assets avoid stale releases."], "Static URL -> security permit rule -> ResourceHttpRequestHandler.", verify="Check every CSS and JS request for 200 rather than 302.", mistake="Debugging a broken layout while its CSS request is redirected to login."),
        L("Design anonymous and authenticated navigation", "The navigation should expose login for anonymous users and identity/logout for authenticated users.", ["sec:authorize evaluates current Authentication during rendering.", "Mustache receives authenticated and displayName model values.", "The server still protects the destination URL."], "Authentication -> view condition -> visible navigation state.", code="auth_nav", verify="Compare rendered source for anonymous and signed-in requests.", mistake="Rendering the full principal object into the page."),
        L("Keep the logout action in the layout", "A POST form in shared navigation makes secure logout available on every authenticated page.", ["Use the configured logout URL consistently.", "Thymeleaf can contribute CSRF to the POST form.", "Mustache needs the token values explicitly."], "Logout form -> LogoutFilter -> session invalidation -> redirect.", code="logout_th", verify="Logout from two different pages.", mistake="Creating a GET logout hyperlink."),
    ]),
    (4, "Render Model Data and Template Logic", [
        L("Read a simple model value", "A template expression should read a presentation value that the controller intentionally supplied.", ["Use th:text for escaped text.", "Mustache double braces also escape by default.", "Provide a harmless fallback for static preview."], "Model pageTitle -> escaped output -> text node.", code="model_attr", verify="Change pageTitle in the controller and observe only the heading.", mistake="Using unescaped output for ordinary strings."),
        L("Use conditions for presentation state", "Conditions choose whether markup appears; they do not grant permission to call an endpoint.", ["Show success messages only when the relevant flag exists.", "Use inverted Mustache sections for an else-like state.", "Keep security policy outside the view."], "Model boolean/message -> conditional markup -> user feedback.", code="mustache_vars", verify="Render with the model value present and absent.", mistake="Hiding an admin button without protecting its URL."),
        L("Iterate over safe view models", "Lists should contain only fields needed by the page and should render escaped values.", ["Prefer lightweight row DTOs over persistent entities.", "Show an explicit empty state.", "Keep iteration markup semantically valid for tables or lists."], "Service result -> controller view model list -> repeated HTML.", verify="Test zero, one, and many list items.", mistake="Triggering lazy repository access from a template loop."),
        L("Bind one form object", "th:object defines the form model; *{...} expressions address its properties.", ["The GET controller must add that attribute.", "The failed POST must return the same attribute name.", "Mustache uses explicit form.property variables but follows the same contract."], "Model form -> th:object -> named input -> @ModelAttribute form.", code="join_th", verify="Rename the model key deliberately and observe the error.", mistake="Using th:object='${member}' while the controller supplies form."),
        L("Understand th:field output", "th:field produces a name, id, and current value appropriate for binding.", ["It reduces mismatch between displayed value and request parameter.", "For passwords, never preserve the raw value after failure.", "Checkboxes and collections need special attention to generated fields."], "DTO property -> th:field -> request parameter -> binder property.", verify="Inspect rendered id and name values.", mistake="Adding a separate conflicting name attribute."),
        L("Render only safe principal data", "The page normally needs a display name and authorities-based flags, not credentials or OAuth tokens.", ["sec:authentication='name' reads the principal name.", "A view model may expose a chosen nickname.", "Never render mpw, provider access token, or raw attributes wholesale."], "Authentication -> selected display fields -> escaped HTML.", code="auth_nav", verify="Search rendered source for password hashes and tokens.", mistake="Serializing MemberSecurityDTO into inline JavaScript."),
        L("Use inline JavaScript sparingly", "Thymeleaf JavaScript inlining can safely serialize model values, but data should remain minimal.", ["Prefer data attributes for small behavior flags.", "Keep secrets and credentials out of the DOM.", "Separate behavior into static .js files when possible."], "Safe model flag -> rendered data attribute -> static script behavior.", verify="Inspect page source for every inline model value.", mistake="Embedding the entire member object for convenience."),
        L("Distinguish request, flash, and session data", "Template variables may originate from request model, one-redirect flash data, or session/authentication state.", ["Ordinary model data ends with the response.", "Flash attributes survive one redirect.", "Authentication survives according to session or remember-me state."], "Controller/model scope determines how long a displayed value exists.", verify="Refresh after a flash message and confirm it disappears.", mistake="Using session storage for every form error."),
        L("Keep templates free of business decisions", "A template may format and select presentation states, but services decide account rules and ownership.", ["Do not calculate roles or password rules in JavaScript alone.", "Do not call repositories from expressions.", "Render the result of a backend decision."], "Service policy -> controller view state -> simple template branch.", verify="Review each template expression and name its model source.", mistake="Reimplementing account eligibility in th:if."),
        L("Build a function connection table", "For every expression, document input model key, rendered result, submitted field, and backend consumer.", ["This table reveals broken names quickly.", "It also makes Thymeleaf-to-Mustache conversion mechanical.", "Keep it beside tests as the UI contract."], "Template function -> HTML effect -> HTTP effect -> backend function.", verify="Create rows for action, field, error, principal, and CSRF.", mistake="Documenting syntax without its request effect."),
    ]),
    (5, "Build the Sign-Up Frontend", [
        L("Read the complete sign-up journey", "The sign-up UI has a GET rendering path, an error return path, and a successful redirect path.", ["GET prepares form DTO.", "Invalid POST returns errors and safe values.", "Valid POST encodes and saves before redirecting to login."], "Frontend form joins the backend MemberService use case; it never stores a member itself.", image="signup-validation-flow.png", verify="Trace one request through each branch.", mistake="Calling sign-up complete when only the page renders."),
        L("Prepare form state on GET", "The GET handler supplies a new DTO under the same name used by the template.", ["Do not create database state on GET.", "Preserve flash data when a redirect intentionally provided it.", "Return a logical view name."], "joinGet -> model form -> th:object / Mustache form variables.", code="model_get", verify="Refresh repeatedly and confirm no database writes.", mistake="Building the DTO inside JavaScript only."),
        L("Choose meaningful form structure", "Use a heading, explanatory text, form, field groups, and one clear primary action.", ["Each input needs a visible label.", "Order fields as users expect: ID, email, password or according to product research.", "Keep secondary navigation outside the primary submission path."], "Semantic HTML -> usable browser form -> expected request parameters.", verify="Navigate the form using only keyboard Tab.", mistake="Using placeholder text as the only label."),
        L("Bind the Thymeleaf form", "th:action builds the endpoint, th:object selects the DTO, and th:field connects properties.", ["The browser receives a normal action and named controls.", "Server errors can attach to the same fields.", "Use password autocomplete appropriate to account creation."], "th:action -> POST /member/join; th:field -> DTO property.", code="join_th", verify="Inspect the final form action, method, names, and hidden CSRF field.", mistake="Writing action and th:action with different URLs."),
        L("Build the Mustache equivalent", "Mustache writes ordinary names and values explicitly and renders explicit error sections.", ["Use the same endpoint and parameter names.", "Add actual CSRF values from the model.", "Do not render the submitted password back."], "{{form.mid}} -> value; name='mid' -> DTO binding.", code="join_mustache", verify="Compare POST bodies from Thymeleaf and Mustache.", mistake="Using {{form.mpw}} as the password value after failure."),
        L("Add browser input hints", "HTML input types, required, minlength, maxlength, and autocomplete improve user experience but are not security enforcement.", ["Use type=email for keyboard and basic format hints.", "Use autocomplete=new-password for creation.", "Match lengths to the server contract so messages do not contradict."], "HTML constraint -> browser guidance; Bean Validation -> enforced server rule.", code="aria", verify="Bypass browser validation and confirm server rejection.", mistake="Assuming required blocks crafted HTTP requests."),
        L("Submit one clear primary action", "A submit button triggers form submission; a reset button often surprises users and is rarely necessary.", ["Disable repeat clicks only as an experience aid.", "The server must still handle duplicate requests safely.", "Show progress without hiding validation errors."], "button type=submit -> form submission -> POST handler.", verify="Double-click under throttled network conditions.", mistake="Using type=button without JavaScript submission logic."),
        L("Handle duplicate ID feedback", "A duplicate detected by the service should return a useful form or field message without exposing internals.", ["Keep email and ID values when safe.", "Clear the password field.", "Use a message that helps correction but avoids stack traces."], "MidExistException -> controller error state -> field/global message.", verify="Submit an existing ID and inspect model and HTML.", mistake="Displaying the repository exception text."),
        L("Use Post/Redirect/Get on success", "Successful creation returns a redirect, and the browser performs a fresh GET of the login page.", ["This prevents refresh from resubmitting the account creation.", "A flash message can explain the next step.", "The response body of the POST is normally empty or minimal."], "MemberService.join -> redirect:/member/login -> GET login model.", code="join_post", verify="Inspect 302 and Location headers.", mistake="Returning member/login directly after save."),
        L("Display the success message once", "A flash attribute lets the login page confirm account creation for the following request.", ["Use role=status for non-urgent feedback.", "Keep the message concise.", "Do not place submitted password or secrets in flash data."], "RedirectAttributes -> flash map -> login template condition.", code="flash", verify="Refresh and confirm the message does not persist indefinitely.", mistake="Putting a success string in a permanent query parameter unnecessarily."),
        L("Protect form values from leakage", "Raw passwords must not appear in URL, logs, HTML value attributes, analytics, or browser-visible JSON.", ["Always use POST for credentials.", "Clear password on every error rendering.", "Avoid logging DTOs whose toString includes mpw."], "Password input -> HTTPS POST -> immediate backend encoding.", verify="Search response source, URL, and logs after a failed form.", mistake="Preserving the password to save retyping."),
        L("Finish with a sign-up UI checklist", "A finished page is accessible, validated, CSRF-protected, error-aware, responsive, and connected to the backend transaction.", ["Test anonymous access and duplicate ID.", "Test malformed input and direct crafted requests.", "Test success redirect and encoded storage using backend tests."], "Frontend behavior + backend invariants = complete sign-up feature.", verify="Run the full sign-up checklist on mobile width and desktop.", mistake="Judging completion only from visual appearance."),
    ]),
    (6, "Show Validation and Feedback", [
        L("BindingResult is the frontend error source", "The controller receives binding and validation errors, then returns them with the form model.", ["A field error identifies object and property.", "A global error describes a form-level rule.", "The template renders messages; it does not create the validation decision."], "Bean Validation -> BindingResult -> th:errors / Mustache error model.", code="join_post", verify="Inspect BindingResult for three invalid fields.", mistake="Running validation only in JavaScript."),
        L("Render field errors beside fields", "Place an understandable message next to the control it describes.", ["Use th:errors to obtain resolved message text.", "Use a consistent CSS class.", "Associate error text with the input for assistive technology."], "BindingResult field error -> rendered paragraph -> user correction.", code="field_state", verify="Trigger an email error and inspect DOM association.", mistake="Showing every error only in an alert at the top."),
        L("Mark invalid visual state", "An invalid class helps sighted users, but color alone must not carry the meaning.", ["Add text and aria-invalid.", "Preserve visible focus indicators.", "Use sufficient contrast for error text and borders."], "#fields.hasErrors -> CSS class -> visible and accessible state.", code="field_state", verify="Review in grayscale and with keyboard focus.", mistake="Using only a red border."),
        L("Render global errors", "Cross-field or use-case errors need a form-level location with a clear summary.", ["Use role=alert only for information that needs immediate announcement.", "Keep field messages beside fields too.", "Do not reveal database details."], "Global ObjectError -> alert region -> corrective action.", code="global_errors", verify="Create a password-confirmation mismatch test.", mistake="Mapping every service failure to a 500 page."),
        L("Preserve only safe entered values", "ID and email may be repopulated after failure; passwords and tokens should not be.", ["Thymeleaf th:field reads the rejected value for normal fields.", "Mustache receives a sanitized view model.", "A redirect loses BindingResult unless special flash handling is designed."], "Rejected field values -> returned view model -> safe re-render.", verify="Fail registration and inspect all input value attributes.", mistake="Returning the raw password in the model."),
        L("Write messages for beginners", "Messages should state what happened and what the user can do next.", ["Prefer 'Use at least 10 characters' over annotation names.", "Use one terminology consistently for User ID and password.", "Avoid blaming language."], "Validation message bundle -> resolved message -> rendered text.", verify="Read every message without seeing the code.", mistake="Displaying 'Size.form.mpw'."),
        L("Translate messages centrally", "Message bundles allow Thymeleaf validation text and view labels to support locales without changing controllers.", ["Use stable message keys.", "Keep technical log text separate from user text.", "Test fallback locale behavior."], "Constraint/message key -> MessageSource -> localized template output.", verify="Render one page in two locales.", mistake="Hard-coding every message in Java controller branches."),
        L("Map errors for Mustache", "Mustache has no direct th:errors equivalent, so adapt BindingResult into explicit booleans and messages.", ["Use a helper or controller advice to avoid repetitive mapping.", "Escape all message text.", "Keep keys such as midError stable."], "BindingResult -> view error map -> Mustache section.", code="join_mustache", verify="Compare Thymeleaf and Mustache error scenarios.", mistake="Passing BindingResult and expecting Mustache magic identical to Thymeleaf."),
        L("Avoid alert-only JavaScript feedback", "Server-rendered inline errors survive disabled JavaScript and work with browser history.", ["JavaScript may enhance focus or summary behavior.", "Do not replace the validation contract with alert().", "Keep server errors visible in the document."], "Server response HTML -> persistent feedback; JS -> optional enhancement.", verify="Disable JavaScript and complete an invalid submission.", mistake="Using only alert('already exists')."),
        L("Test the error loop end to end", "An error-loop test asserts status 200, same view, model errors, escaped values, and a blank password.", ["Use a valid CSRF token so validation is reached.", "Assert field errors by name.", "Inspect rendered HTML for labels and messages."], "MockMvc POST -> BindingResult -> rendered template assertions.", code="mockmvc_error", verify="Run invalid ID, password, and email together.", mistake="Expecting a redirect for ordinary validation failure."),
    ]),
    (7, "Build Login and Session-Aware UI", [
        L("Read the login-to-UI flow", "The login page offers local form and Kakao choices; both can converge into Authentication and an HttpSession.", ["Spring Security processes credentials and OAuth2 callbacks.", "The frontend shows errors and follows redirects.", "JSESSIONID identifies server-side session state."], "Login UI -> Security filters -> Authentication -> session -> protected UI.", image="login-session-ui-flow.png", verify="Trace local success, Kakao success, and one error.", mistake="Writing credential verification in template JavaScript."),
        L("Render GET /member/login", "The controller only renders the custom page; Spring Security processes POST /member/login.", ["Keep the GET public.", "Show error/logout messages from parameters or model.", "Do not add a POST login controller unless intentionally replacing the processing flow."], "GET controller -> login template; POST -> UsernamePasswordAuthenticationFilter.", verify="Set breakpoints and compare GET with POST.", mistake="Calling MemberService from the login form controller."),
        L("Use exact credential names", "Default form login expects username and password parameters.", ["The visible label may say User ID while name remains username.", "Changing parameter names requires matching security configuration.", "Mustache and Thymeleaf submit the same names."], "input name=username/password -> authentication filter token.", code="login_th", verify="Inspect Form Data on login POST.", mistake="Naming the field mid without configuring usernameParameter."),
        L("Use password-safe input behavior", "The password control should use type=password and current-password autocomplete.", ["This supports password managers.", "Do not repopulate on error.", "A show-password button must preserve labels, focus, and aria state."], "Password input -> raw candidate -> PasswordEncoder.matches in backend.", code="password_toggle", verify="Test keyboard and screen-reader state of the toggle.", mistake="Using type=text as in the current login template."),
        L("Render a neutral login error", "A common message should not reveal whether the username exists.", ["Use param.error or a failure-handler flag.", "Focus the heading or message thoughtfully after failure.", "Never echo the password."], "AuthenticationFailureHandler -> redirect ?error -> template message.", code="login_messages", verify="Compare wrong user and wrong password output.", mistake="Showing 'account exists, password wrong'."),
        L("Offer remember-me intentionally", "The checkbox name remember-me tells Spring Security to issue a long-lived credential after successful login.", ["Explain shared-device risk.", "Do not preselect it.", "The backend companion covers persistent token storage and revocation."], "remember-me parameter -> RememberMeServices -> cookie/token repository.", code="login_th", verify="Compare response cookies with checkbox on and off.", mistake="Calling JSESSIONID the remember-me cookie."),
        L("Show the Kakao entry as a link", "The Kakao button starts at Spring Security's authorization endpoint rather than posting Kakao credentials.", ["Use a normal link so redirects work without JavaScript.", "Provide recognizable but accessible text.", "Keep local login available according to product choice."], "Link -> OAuth2AuthorizationRequestRedirectFilter -> Kakao.", code="social_link", verify="Inspect the first 302 Location.", mistake="Pointing the button directly at the callback URL."),
        L("Render the authenticated identity", "After login, navigation can display a safe principal name and authenticated actions.", ["sec:authentication reads current Authentication.", "Mustache receives a small display model.", "Do not trust displayed name for backend ownership; backend reads Authentication."], "Authentication -> sec:authentication/name -> visible greeting.", code="auth_nav", verify="Login as two users and compare source.", mistake="Submitting displayed username as the authorization source."),
        L("Handle the protected-page redirect", "An anonymous request may be saved, redirected to login, then resumed after authentication.", ["Explain the destination to avoid confusing navigation.", "Avoid open redirect parameters.", "Test direct visits to protected board actions."], "RequestCache -> login -> success handler -> saved request or default URL.", verify="Open a protected URL in a fresh private window.", mistake="Hard-coding a success URL that breaks every saved request flow."),
        L("Finish the login UI checklist", "The page needs correct processing URL, field names, CSRF, errors, remember-me choice, social link, and accessible controls.", ["Test local success and failure.", "Test Kakao entry and failure feedback.", "Test session-aware navigation and logout."], "Frontend checks align with backend Chapters 6 through 8.", verify="Complete the checklist without reading server code.", mistake="Treating a pretty login card as a completed authentication feature."),
    ]),
    (8, "Connect CSRF, Logout, Remember-Me, and JavaScript", [
        L("Let Thymeleaf integrate form CSRF", "A Thymeleaf POST form processed with Spring Security can receive the hidden CSRF field automatically.", ["Inspect rendered HTML rather than assuming.", "The token must match the session/request context.", "Do not keep a stale token in copied static HTML."], "th:action POST form -> RequestDataValueProcessor -> hidden CSRF -> CsrfFilter.", verify="View source and locate the hidden token.", mistake="Adding a hard-coded token value."),
        L("Expose CSRF to JavaScript safely", "Meta tags can publish the current token and required header name for same-origin scripts.", ["The token is not a substitute for authentication.", "XSS can read DOM values, so output escaping remains essential.", "Load the script with defer so the document metadata exists."], "_csrf model -> meta content -> JS request header -> CsrfFilter.", code="csrf_meta", verify="Inspect token/header metadata after page render.", mistake="Printing the token to console logs."),
        L("Configure Axios without mixing HTML and JS", "A static JavaScript file reads meta tags and sets the dynamic header on Axios.", ["Keep <script> tags in HTML, not inside security.js.", "Guard for pages where Axios or metadata is absent.", "Use the header name supplied by Spring."], "Rendered meta -> security.js -> axios defaults -> state-changing request.", code="csrf_js", verify="Open security.js directly and confirm it contains valid JavaScript only.", mistake="Leaving the current <script ...> line inside the .js file."),
        L("Send CSRF with fetch", "Fetch requests must include the token header for protected state-changing methods.", ["Use same-origin credentials behavior deliberately.", "Set Content-Type only when the controller expects that body format.", "Handle 403 separately from validation 400 responses."], "DOM token -> fetch header -> CsrfFilter -> controller.", code="fetch_csrf", verify="Compare POST with header present and absent.", mistake="Disabling CSRF to make JavaScript simpler."),
        L("Use POST logout", "Logout changes authenticated state and should be submitted as a CSRF-protected POST.", ["Put the form in shared authenticated navigation.", "Use the exact configured logout URL.", "A success redirect can show param.logout feedback."], "Logout form -> LogoutFilter -> SecurityContext/session cleanup.", code="logout_th", verify="Replay an old session after logout.", mistake="Using an <a href='/logout'> GET link."),
        L("Adapt logout to Mustache", "Mustache needs authentication and CSRF values in its model to render the equivalent form.", ["Use a section to show the action only when authenticated.", "Never use a static token.", "The backend endpoint is identical."], "CommonViewModel -> Mustache section/hidden field -> same LogoutFilter.", code="logout_mustache", verify="Inspect the Mustache POST body.", mistake="Creating a Mustache-only logout controller."),
        L("Explain remember-me to users", "The UI should describe persistence without promising that a session itself lasts 30 days.", ["Use wording such as Keep me signed in.", "Avoid on shared devices guidance when appropriate.", "Provide logout that revokes the persistent token."], "Checkbox -> backend persistent remember-me mechanism.", verify="Test after deleting JSESSIONID but retaining remember-me.", mistake="Labeling it automatic login without explaining persistence."),
        L("Separate 403 from field errors", "CSRF failure occurs before the controller, while validation errors occur after binding.", ["A missing token usually yields 403.", "A bad field should return the form with BindingResult.", "Frontend diagnostics should identify which response occurred."], "CsrfFilter precedes MemberController and BindingResult.", verify="Trigger each failure and compare status and logs.", mistake="Displaying 'invalid email' for a CSRF rejection."),
        L("Keep cookies out of JavaScript", "HttpOnly session and remember-me cookies are designed to be sent by the browser without script access.", ["Frontend code does not need to parse JSESSIONID.", "Use the rendered Authentication state or protected endpoints.", "Cookie security attributes are configured server-side."], "Browser cookie jar -> automatic Cookie header -> session lookup.", verify="Confirm document.cookie cannot read HttpOnly authentication cookies.", mistake="Using JSESSIONID as a visible user identifier."),
        L("Build one safe request helper", "A small module can apply CSRF and common error handling consistently without hiding HTTP semantics.", ["Keep method, URL, and content type explicit at call sites.", "Do not attach tokens to third-party origins.", "Test 302, 400, 403, and 500 handling."], "Frontend helper -> explicit request -> security filters -> controller.", verify="Review all state-changing JS calls for the helper.", mistake="Setting the CSRF header on cross-origin requests."),
    ]),
    (9, "Present Kakao Social Login", [
        L("The button starts a redirect journey", "Social login is navigation through Spring Security and Kakao, not an AJAX password submission.", ["A normal anchor works when JavaScript is disabled.", "The browser will leave the application and return.", "State tracking protects the authorization journey."], "Kakao link -> OAuth2 redirect filter -> provider -> callback.", code="social_link", verify="Follow redirects in the Network panel.", mistake="Collecting a Kakao password in your form."),
        L("Explain the transition to users", "The label should say Continue with Kakao and make the external step understandable.", ["Keep local and social choices visually separated but equal in meaning.", "Avoid implying that the application receives Kakao credentials.", "Provide a clear way back after cancellation."], "Frontend choice -> provider consent -> application session on success.", verify="Cancel at Kakao and observe the return behavior.", mistake="Using only an icon with no accessible name."),
        L("Do not depend on email display", "The UI must handle a Kakao account whose email is missing or not shared.", ["Ask for required profile data during onboarding if necessary.", "Do not expose raw provider attribute structures.", "Use the backend provider subject for identity."], "OAuth2 principal -> safe profile view model -> onboarding template.", verify="Test mocked OAuth2 data without email.", mistake="Rendering null or crashing because kakao_account.email is absent."),
        L("Render first-login onboarding explicitly", "If profile completion is required, use a dedicated state and page rather than the 1111 password sentinel.", ["Explain what information is still needed.", "Do not ask for the Kakao password.", "A local password option needs a deliberate account-linking design."], "profileCompleted=false -> success handler/onboarding route -> safe form.", verify="Test new and returning social users.", mistake="Redirecting based on PasswordEncoder.matches('1111', ...)."),
        L("Show a neutral OAuth2 failure", "The login page should explain that social sign-in did not finish and offer retry or local login.", ["Do not expose access tokens, client secret, or provider stack traces.", "Server logs identify authorization, token, user-info, or database failure.", "Keep user copy neutral for cancellation versus technical failure if uncertain."], "OAuth2 failure handler -> safe error code/model -> login template.", code="login_messages", verify="Simulate provider denial and application failure.", mistake="Displaying KOE error internals to end users."),
        L("Return to a safe destination", "After Kakao success, send users to a fixed safe page or a validated saved request.", ["Avoid open redirect parameters.", "Show authenticated navigation immediately.", "Use Post/Redirect/Get-like browser navigation semantics even though OAuth2 uses several redirects."], "Authentication success -> session -> safe redirect -> protected template.", verify="Test a crafted redirect parameter.", mistake="Trusting an arbitrary returnUrl."),
        L("Display linked-provider status carefully", "An account settings page may show that Kakao is linked without exposing provider identifiers or tokens.", ["Show provider name and meaningful last-used time if product needs it.", "Require reauthentication for link/unlink.", "Backend owns the provider-subject mapping."], "OAuthIdentity state -> safe settings DTO -> template.", verify="Inspect source for provider subject and tokens.", mistake="Putting raw OAuth2 attributes into a data-* attribute."),
        L("Complete the social-login UI checklist", "The frontend covers entry, consent transition, cancellation, success navigation, onboarding, errors, and authenticated state.", ["Test with missing optional profile data.", "Test direct callback misuse at backend level.", "Keep local and social login experiences consistent."], "Frontend social flow complements backend Chapters 11 and 12.", verify="Run every social UI state using mocked identities.", mistake="Testing only one already-authorized Kakao account."),
    ]),
    (10, "Make Authentication UI Accessible and Responsive", [
        L("Use labels, not placeholders", "A persistent label tells every user what a field means before, during, and after typing.", ["Connect label for to input id.", "Use placeholder only as an optional example.", "Keep terminology consistent with validation messages."], "Accessible label -> form control name -> backend parameter.", code="aria", verify="Remove placeholders and confirm the form remains understandable.", mistake="Using USER ID placeholder as the only label."),
        L("Connect help and error text", "aria-describedby can associate guidance and errors with the field.", ["Set aria-invalid when the server reports an error.", "Do not duplicate announcements unnecessarily.", "Keep IDs unique after layout composition."], "BindingResult -> error element/id -> input accessibility relationship.", code="aria", verify="Inspect the accessibility tree.", mistake="Adding ARIA while leaving broken native labels."),
        L("Preserve visible keyboard focus", "Keyboard users must see which link, input, or button is active.", ["Use :focus-visible for a strong outline.", "Do not remove outlines without replacement.", "Follow a logical DOM order."], "CSS focus state -> usable navigation -> successful submission.", code="auth_css", verify="Complete sign-up without a mouse.", mistake="Setting outline:none globally."),
        L("Build a responsive auth shell", "A narrow, centered card can work across mobile and desktop when width and spacing are fluid.", ["Use width:min(100%, max-width).", "Add page padding so controls never touch screen edges.", "Keep tap targets comfortably sized."], "Responsive CSS -> same semantic form -> all viewport sizes.", code="auth_css", verify="Test 320px, 768px, and wide desktop widths.", mistake="Using fixed pixel width larger than a phone."),
        L("Use semantic status regions", "Success messages can use role=status; urgent errors may use role=alert when immediate announcement is appropriate.", ["Do not make every text block live.", "Place focus deliberately after navigation.", "Keep messages visible, not only spoken."], "Backend result/error -> semantic region -> assistive announcement.", code="flash", verify="Test with a screen reader or accessibility inspector.", mistake="Using alert() popups for every message."),
        L("Support password managers", "Correct autocomplete values improve both usability and password strength.", ["Use new-password for account creation.", "Use current-password for login.", "Keep username and password fields in the same logical form."], "Browser password manager -> named inputs -> secure backend match.", code="login_th", verify="Test save/fill behavior in a browser profile.", mistake="Setting autocomplete=off on login credentials."),
        L("Use progressive enhancement", "The server-rendered form should work without JavaScript; scripts may add polish such as password visibility or focus management.", ["Keep form action and submit button functional.", "Do not require Axios for ordinary sign-up/login.", "Handle enhancement failure gracefully."], "HTML baseline -> backend request; JavaScript -> optional behavior.", verify="Disable JavaScript and run sign-up and login.", mistake="Attaching all submission to a click handler without fallback."),
        L("Test content, not only colors", "Responsive and accessible review includes wording, reading order, zoom, contrast, and error recovery.", ["Zoom to 200 percent.", "Test reduced motion preferences if animations exist.", "Use automated checks as support, not the entire audit."], "Human-facing output is part of the authentication contract.", verify="Run keyboard, zoom, mobile, and error-message checks.", mistake="Calling Bootstrap classes automatically accessible."),
    ]),
    (11, "Convert the Complete UI to Mustache", [
        L("Create a common Mustache view model", "Mustache needs explicit values for authenticated state, display name, CSRF, form values, and errors.", ["A ControllerAdvice can provide common values.", "Keep per-page fields in the page controller.", "Never add password hashes or tokens unrelated to CSRF."], "Authentication/CsrfToken -> CommonViewModel -> Mustache sections.", code="common_model", verify="Print model key names without secret values in a test.", mistake="Passing Authentication object directly and exploring it in templates."),
        L("Convert variables and conditions", "Replace th:text and th:if with escaped variables, sections, and inverted sections.", ["Model names remain stable.", "Provide booleans for complex presentation decisions.", "Avoid logic-heavy nested sections."], "Thymeleaf expression -> equivalent Mustache model key/section.", code="mustache_vars", verify="Convert login messages and empty states.", mistake="Using unescaped triple braces by default."),
        L("Convert sign-up binding", "Write each input name and safe value explicitly while preserving the POST contract.", ["Use form.mid and form.email.", "Leave password value blank.", "Render field-specific error sections."], "Mustache input names -> same MemberJoinDTO binding.", code="join_mustache", verify="Compare the submitted parameter map with Thymeleaf.", mistake="Changing mpw to password during conversion without backend change."),
        L("Convert login", "The Mustache login form still posts username, password, remember-me, and CSRF to Spring Security.", ["The POST is not handled by a Mustache controller.", "Use the same local and Kakao entry URLs.", "Render safe error/logout flags."], "Mustache form -> same UsernamePasswordAuthenticationFilter.", code="login_mustache", verify="Run formLogin integration tests against rendered names.", mistake="Creating /mustache/member/login processing URL unnecessarily."),
        L("Convert authentication navigation", "Supply authenticated and displayName fields and use sections for visible state.", ["Keep endpoint security in the filter chain.", "Render the POST logout form only for authenticated state.", "Escape the display name."], "Authentication -> small model -> Mustache navigation sections.", code="logout_mustache", verify="Compare anonymous and authenticated HTML.", mistake="Passing role strings from the browser back as authority proof."),
        L("Convert CSRF", "Expose the actual parameter name and token, then render a hidden input in every state-changing form.", ["Do not assume the name is forever _csrf.", "JavaScript can receive equivalent meta values.", "Test a missing-token negative case."], "CsrfToken -> model -> hidden input/header -> CsrfFilter.", code="common_model", verify="Inspect join, login, and logout forms.", mistake="Using a random UUID as a fake CSRF token."),
        L("Convert layout and fragments", "Mustache partials can replace common navigation and repeated page chrome.", ["Prepare the partial with required model keys.", "Keep one document root.", "Avoid duplicating CSS and JavaScript includes."], "Common model + partial -> final page layout.", verify="Render every page and count duplicate asset tags.", mistake="Copying the full layout into each .mustache file."),
        L("Run the same contract tests", "The engine conversion is complete only when URLs, parameters, errors, security behavior, and accessibility match.", ["Run GET/view tests.", "Run invalid POST and CSRF tests.", "Run local login, social entry, authenticated navigation, and logout tests."], "Same backend contract lets one behavior suite validate both editions.", verify="Create a side-by-side acceptance checklist.", mistake="Comparing screenshots while ignoring submitted requests."),
    ]),
    (12, "Test, Debug, and Release the Frontend", [
        L("Test the GET contract", "A view test asserts status, logical view name, required model attributes, and important rendered controls.", ["Keep assertions focused on behavior.", "Verify field names and action URLs.", "Avoid brittle full-document string equality."], "MockMvc GET -> controller -> model -> rendered content assertions.", code="mockmvc_view", verify="Add tests for join and login GET.", mistake="Testing only that status is 200."),
        L("Test the invalid POST loop", "A failed sign-up should return the same view with field errors and no service write.", ["Include csrf() so validation is reached.", "Assert field errors by object and property.", "Confirm the password is not rendered."], "MockMvc POST -> BindingResult -> template error output.", code="mockmvc_error", verify="Assert repository count is unchanged.", mistake="Expecting 302 for invalid input."),
        L("Test security-visible states", "Render pages as anonymous, local user, remembered user, and OAuth2 user where the UI differs.", ["Assert login versus logout navigation.", "Assert safe principal display.", "Do not use view tests as the only authorization tests."], "Test Authentication -> sec:authorize/model booleans -> rendered fragments.", verify="Cover every navigation state.", mistake="Treating hidden buttons as proof endpoints are protected."),
        L("Use browser devtools as a request debugger", "The Network, Application, Elements, and Accessibility panels expose the real frontend contract.", ["Network shows status, redirects, form data, and headers.", "Application shows cookies and attributes.", "Elements shows rendered names and CSRF fields."], "Browser evidence links visible UI to backend processing stage.", verify="Capture one annotated sign-up and login trace.", mistake="Looking only at the final URL."),
        L("Diagnose the common status codes", "A frontend diagnosis begins with status and redirect chain before changing templates.", ["302 often indicates login or redirect success.", "403 suggests CSRF or authorization.", "404 suggests URL/view/static resource mismatch.", "500 requires the earliest server exception."], "Status -> failing layer -> smallest corrective edit.", verify="Intentionally produce one of each status.", mistake="Editing CSS for an HTTP routing problem."),
        L("Check production asset and cookie behavior", "Cloud release must load assets over HTTPS, generate correct external URLs, and preserve secure session behavior.", ["Look for mixed content and CDN failures.", "Inspect Secure, HttpOnly, and SameSite cookie flags.", "Verify Kakao redirect starts from the public host."], "Production proxy/config -> rendered URLs/cookies -> browser behavior.", verify="Run tests through the actual reverse proxy.", mistake="Testing only localhost."),
        L("Run the final frontend acceptance journey", "A beginner should be able to join, see errors, log in locally, return through remember-me, log out, log in with Kakao, and use the app on mobile.", ["Record expected request and UI state at every step.", "Confirm no credentials or hashes appear in source or logs.", "Keep evidence with the release build."], "Frontend acceptance completes the backend security mechanism.", verify="Run the journey in a fresh private browser profile.", mistake="Reusing an old authenticated session for every test."),
        L("Use both books as one system", "The frontend companion explains what the browser renders and submits; the backend book explains how the server validates, authenticates, stores, and authorizes it.", ["Follow cross-reference boxes when a template function reaches a security or service boundary.", "Return to this book when backend behavior needs a user-facing state.", "Extend from stable HTTP and model contracts rather than engine-specific shortcuts."], "Frontend function <-> HTTP contract <-> backend function.", verify="Explain one complete flow without skipping a layer.", mistake="Thinking frontend and backend authentication are separate products."),
    ]),
]


def header(c, chapter, title, page_num):
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 30, PAGE_W, 30, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(MARGIN, PAGE_H - 19, f"CHAPTER {chapter}  |  {ascii_safe(title).upper()}")
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 19, "THYMELEAF + MUSTACHE FRONTEND COMPANION")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 19, str(page_num))


def draw_image(c, filename, y, max_h=260):
    path = IMAGE_DIR / filename
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = min(CONTENT_W / iw, max_h / ih)
    w, h = iw * scale, ih * scale
    c.drawImage(image, MARGIN + (CONTENT_W - w) / 2, y - h,
                width=w, height=h, preserveAspectRatio=True, mask="auto")
    return y - h - 9


def render_lesson(c, chapter, chapter_title, lesson, page_num, index):
    header(c, chapter, chapter_title, page_num)
    bookmark = f"frontend-p{page_num}"
    c.bookmarkPage(bookmark)
    if index == 0:
        c.addOutlineEntry(f"Chapter {chapter}: {chapter_title}", bookmark, level=0)

    y = PAGE_H - 61
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN, y, f"LESSON {chapter}.{index + 1}")
    y -= 25
    title = ascii_safe(lesson["title"])
    size = 18 if len(title) < 50 else 15
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", size)
    c.drawString(MARGIN, y, title)
    y -= 17
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.line(MARGIN, y, MARGIN + 72, y)
    y -= 17

    c.setFillColor(LIGHT_BLUE)
    c.roundRect(MARGIN, y - 51, CONTENT_W, 51, 8, stroke=0, fill=1)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8.3)
    c.drawString(MARGIN + 12, y - 15, "FRONTEND IDEA")
    draw_wrapped(c, lesson["summary"], MARGIN + 12, y - 31,
                 CONTENT_W - 24, size=9.0, leading=11.2, max_lines=2)
    y -= 67

    if lesson.get("image"):
        y = draw_image(c, lesson["image"], y, max_h=245)
    else:
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(MARGIN, y, "From screen to server")
        y -= 17
        for detail in lesson["details"]:
            y = draw_bullet(c, detail, MARGIN, y, CONTENT_W, size=8.8) - 5

    if lesson.get("code"):
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10.2)
        c.drawString(MARGIN, y, "Project code")
        y -= 9
        y = draw_code(c, CODES[lesson["code"]], MARGIN, y, CONTENT_W)
    elif not lesson.get("image"):
        c.setFillColor(LIGHT_GOLD)
        c.roundRect(MARGIN, y - 45, CONTENT_W, 45, 7, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#8A6100"))
        c.setFont("Helvetica-Bold", 8.2)
        c.drawString(MARGIN + 11, y - 15, "FUNCTION CONNECTION")
        draw_wrapped(c, lesson["connection"], MARGIN + 11, y - 30,
                     CONTENT_W - 22, size=8.3, leading=10, max_lines=2)

    panel_y = 40
    panel_h = 103
    c.setFillColor(LIGHT_TEAL)
    c.roundRect(MARGIN, panel_y, CONTENT_W, panel_h, 8, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(MARGIN + 11, panel_y + panel_h - 17, "BACKEND COMPANION")
    draw_wrapped(c, lesson.get("ref") or REF[chapter], MARGIN + 117,
                 panel_y + panel_h - 17, CONTENT_W - 128,
                 size=7.9, leading=9.4, color=INK, max_lines=2)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(MARGIN + 11, panel_y + 52, "CHECK")
    draw_wrapped(c, lesson["verify"], MARGIN + 70, panel_y + 52,
                 CONTENT_W - 82, size=8.1, leading=9.6, color=INK, max_lines=2)
    c.setFillColor(colors.HexColor("#B23B3B"))
    c.setFont("Helvetica-Bold", 8.1)
    c.drawString(MARGIN + 11, panel_y + 20, "AVOID")
    draw_wrapped(c, lesson["mistake"], MARGIN + 70, panel_y + 20,
                 CONTENT_W - 82, size=8.0, leading=9.4, color=INK, max_lines=2)


def front_title(c, title, page_num):
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 12, PAGE_W, 12, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, PAGE_H - 62, title)
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.line(MARGIN, PAGE_H - 77, MARGIN + 82, PAGE_H - 77)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 19, str(page_num))


def front_1(c, page_num):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 25, PAGE_W, 25, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(48, PAGE_H - 142, "THYMELEAF & MUSTACHE")
    c.drawString(48, PAGE_H - 180, "FRONTEND COMPANION")
    c.setFillColor(colors.HexColor("#9EDFD8"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(49, PAGE_H - 218, "Build the browser side of secure sign-up and login")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 10)
    draw_wrapped(c, "A beginner guide to forms, model data, validation errors, layouts, CSRF, session-aware navigation, Kakao entry, accessibility, testing, and backend connections.", 49, PAGE_H - 257, PAGE_W - 98, size=10, leading=14, color=WHITE)
    y = 420
    for label, desc, fill in [
        ("RENDER", "Controller model -> template -> HTML", LIGHT_BLUE),
        ("SUBMIT", "Form fields -> HTTP request -> validation", LIGHT_TEAL),
        ("AUTHENTICATE", "Login choices -> Spring Security -> session UI", LIGHT_GOLD),
    ]:
        c.setFillColor(fill)
        c.roundRect(49, y, PAGE_W - 98, 62, 9, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(65, y + 34, label)
        c.setFont("Helvetica", 9)
        c.drawString(175, y + 34, desc)
        y -= 82
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8.5)
    c.drawString(49, 52, "Companion to Build Sign-Up and Login You Can Adapt | 116 pages")


def front_2(c, page_num):
    front_title(c, "How to use this companion", page_num)
    y = PAGE_H - 112
    paras = [
        "This book begins where the backend guide meets the browser. Every lesson names the visible frontend function, the HTTP effect it creates, and the backend class or Spring Security filter that consumes it.",
        "Follow the Thymeleaf path first because it matches the current marketwatcher project. Chapter 11 converts the complete interface to Mustache without changing the sign-up service, authentication mechanism, session, or OAuth2 flow.",
        "Use browser devtools throughout. The rendered HTML and Network panel are the bridge between a template expression and a backend method call.",
    ]
    for text in paras:
        y = draw_wrapped(c, text, MARGIN, y, CONTENT_W, size=10.2, leading=14)
        y -= 18
    c.setFillColor(LIGHT_GOLD)
    c.roundRect(MARGIN, y - 190, CONTENT_W, 190, 9, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 15, y - 25, "Read each lesson in four passes")
    yy = y - 54
    for number, text in enumerate([
        "Screen: What does the person see or do?",
        "HTML: What is rendered and submitted?",
        "HTTP: What method, URL, fields, cookies, and status appear?",
        "Backend: Which filter, controller, service, or session function receives it?",
    ], 1):
        c.setFillColor(BLUE)
        c.circle(MARGIN + 28, yy + 3, 10, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(MARGIN + 28, yy, str(number))
        c.setFillColor(INK)
        c.setFont("Helvetica", 9.5)
        c.drawString(MARGIN + 48, yy, text)
        yy -= 34


def front_3(c, page_num):
    front_title(c, "How this book links to the backend book", page_num)
    rows = [
        ("Frontend Chapters 1-4", "Backend 1, 2, 4, 6-8", "Requests, model, route policy, principal, session"),
        ("Frontend Chapters 5-6", "Backend 3-5", "DTO boundary, sign-up transaction, password encoding"),
        ("Frontend Chapters 7-8", "Backend 6-10", "Login filters, UserDetails, cookies, logout, remember-me"),
        ("Frontend Chapter 9", "Backend 11-12", "Kakao OAuth2, social identity, onboarding"),
        ("Frontend Chapters 10-11", "Backend 1 and 13", "HTTP meaning and template-engine adaptation"),
        ("Frontend Chapter 12", "Backend 14-15", "Tests, diagnostics, and production release"),
    ]
    y = PAGE_H - 118
    for front, back, meaning in rows:
        c.setFillColor(LIGHT_BLUE if int(front.split()[-1].split('-')[0]) % 2 else LIGHT_TEAL)
        c.roundRect(MARGIN, y - 77, CONTENT_W, 67, 8, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9.3)
        c.drawString(MARGIN + 13, y - 27, front)
        c.setFillColor(TEAL)
        c.drawString(MARGIN + 210, y - 27, back)
        c.setFillColor(INK)
        c.setFont("Helvetica", 8.5)
        c.drawString(MARGIN + 13, y - 49, meaning)
        y -= 82
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(MARGIN, 55, "Every lesson page includes a specific backend chapter and page range.")


def front_image(c, title, page_num, filename, bullets):
    front_title(c, title, page_num)
    image = ImageReader(str(IMAGE_DIR / filename))
    iw, ih = image.getSize()
    scale = min(CONTENT_W / iw, 430 / ih)
    w, h = iw * scale, ih * scale
    c.drawImage(image, MARGIN + (CONTENT_W - w) / 2, PAGE_H - 115 - h,
                width=w, height=h, preserveAspectRatio=True, mask="auto")
    y = PAGE_H - 132 - h
    for bullet in bullets:
        y = draw_bullet(c, bullet, MARGIN, y, CONTENT_W, size=8.9) - 5


def front_6(c, page_num):
    front_title(c, "Function connection map", page_num)
    rows = [
        ("th:action / action", "Creates form URL", "Security filter or controller route"),
        ("th:object", "Selects form model", "@ModelAttribute DTO"),
        ("th:field / name", "Creates submitted parameter", "Spring data binder"),
        ("th:errors / error section", "Shows validation message", "BindingResult"),
        ("sec:authorize / authenticated", "Chooses visible navigation", "Authentication"),
        ("CSRF hidden field/meta", "Adds request token", "CsrfFilter"),
        ("remember-me checkbox", "Requests persistence", "RememberMeServices"),
        ("Kakao link", "Starts authorization", "OAuth2 redirect filter"),
        ("POST logout form", "Ends authenticated state", "LogoutFilter"),
    ]
    y = PAGE_H - 108
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN, y, "TEMPLATE FUNCTION")
    c.drawString(MARGIN + 175, y, "BROWSER EFFECT")
    c.drawString(MARGIN + 330, y, "BACKEND CONSUMER")
    y -= 18
    for a, b, d in rows:
        c.setFillColor(PANEL if int((PAGE_H - y) / 18) % 2 else LIGHT_BLUE)
        c.rect(MARGIN, y - 35, CONTENT_W, 35, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Helvetica", 7.9)
        c.drawString(MARGIN + 7, y - 21, a)
        c.drawString(MARGIN + 175, y - 21, b)
        c.drawString(MARGIN + 330, y - 21, d)
        y -= 39


def front_7(c, page_num):
    front_title(c, "Frontend vocabulary", page_num)
    terms = [
        ("Template", "A server-side file that combines markup with model values."),
        ("Rendered HTML", "The ordinary HTML response after template processing."),
        ("Model", "Named values supplied by a controller for one rendering."),
        ("Binding", "Mapping request parameters into a Java object."),
        ("BindingResult", "Errors and rejected values from binding and validation."),
        ("Fragment / partial", "Reusable server-rendered markup."),
        ("Flash attribute", "Data available after one redirect."),
        ("CSRF token", "A request value checked for cookie-authenticated state changes."),
        ("Principal", "The identity inside current Authentication."),
        ("Progressive enhancement", "A working HTML baseline improved by optional JavaScript."),
    ]
    y = PAGE_H - 108
    for term, meaning in terms:
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9.2)
        c.drawString(MARGIN, y, term)
        c.setFillColor(INK)
        y = draw_wrapped(c, meaning, MARGIN + 125, y, CONTENT_W - 125,
                         size=8.9, leading=11)
        c.setStrokeColor(LINE)
        c.line(MARGIN, y - 4, PAGE_W - MARGIN, y - 4)
        y -= 20


def front_8(c, page_num):
    front_title(c, "Contents", page_num)
    y = PAGE_H - 108
    start = 9
    for number, title, lessons in CHAPTERS:
        c.setFillColor(BLUE if number % 2 else TEAL)
        c.setFont("Helvetica-Bold", 9.3)
        c.drawString(MARGIN, y, f"{number:02d}")
        c.setFillColor(NAVY)
        c.drawString(MARGIN + 32, y, title)
        c.setStrokeColor(LINE)
        c.line(MARGIN + 255, y + 2, PAGE_W - MARGIN - 30, y + 2)
        c.setFillColor(MUTED)
        c.drawRightString(PAGE_W - MARGIN, y, str(start))
        y -= 34
        start += len(lessons)
    c.setFillColor(LIGHT_GOLD)
    c.roundRect(MARGIN, 56, CONTENT_W, 50, 8, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica", 8.4)
    c.drawString(MARGIN + 12, 80, "Each lesson maps a screen or template function to its HTTP and backend effect.")


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("Thymeleaf and Mustache Frontend Companion")
    c.setAuthor("marketwatcher project guide")
    c.setSubject("Beginner frontend companion for the Spring authentication backend guide")

    page = 1
    front_1(c, page); c.showPage(); page += 1
    front_2(c, page); c.showPage(); page += 1
    front_3(c, page); c.showPage(); page += 1
    front_image(c, "Server-rendered frontend data flow", page, "frontend-data-flow.png", [
        "A page request reaches security and the controller before a template renders.",
        "Invalid forms loop back with errors; successful forms change state and redirect.",
        "The browser receives HTML, cookies, and redirects - not Java objects.",
    ]); c.showPage(); page += 1
    front_image(c, "Two template engines, one backend", page, "thymeleaf-mustache-one-backend.png", [
        "Thymeleaf and Mustache read the same conceptual model.",
        "They produce the same field names, URLs, and HTTP requests.",
        "Security, sessions, controllers, services, and repositories remain backend responsibilities.",
    ]); c.showPage(); page += 1
    front_6(c, page); c.showPage(); page += 1
    front_7(c, page); c.showPage(); page += 1
    front_8(c, page); c.showPage(); page += 1

    for chapter, title, lessons in CHAPTERS:
        for index, lesson in enumerate(lessons):
            render_lesson(c, chapter, title, lesson, page, index)
            c.showPage()
            page += 1
    c.save()

    reader = PdfReader(str(OUTPUT))
    expected = 116
    if len(reader.pages) != expected:
        raise RuntimeError(f"Expected {expected} pages, created {len(reader.pages)}")
    if not BACKEND_PDF.exists():
        raise RuntimeError("Backend companion PDF is missing")
    print(f"Created {OUTPUT}")
    print(f"Pages: {len(reader.pages)}")
    print(f"Bytes: {OUTPUT.stat().st_size}")


if __name__ == "__main__":
    build()
