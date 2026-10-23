package com.stock.marketwatcher.security;

import com.stock.marketwatcher.domain.Member;
import com.stock.marketwatcher.dto.MemberSecurityDTO;
import com.stock.marketwatcher.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import com.stock.marketwatcher.domain.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.stream.Collectors;

@Log4j2
@Service
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

    private static final String DEMO_USERNAME = "user10";
    private static final String DEMO_PASSWORD = "4321";
//
//    private final String encodedPassword;

    private final MemberRepository memberRepository;


    @Override
    public UserDetails loadUserByUsername(String username)
            throws UsernameNotFoundException {

        log.info("loadUserByUsername: {}", username);

        Optional<Member> result = memberRepository.getWithRoles(username);

//        if (!DEMO_USERNAME.equals(username)) {
//            throw new UsernameNotFoundException(
//                    "User not found: " + username);
//        }
//
//        return User.builder()
//                .username(DEMO_USERNAME)
//                .password(encodedPassword)
//                .authorities("ROLE_USER")
//                .build();
//    }

        if (result.isEmpty()) {
            throw new UsernameNotFoundException("username is not found....");
        }

        Member member = result.get();

        MemberSecurityDTO memberSecurityDTO = new MemberSecurityDTO(
                member.getMid(),
                member.getMpw(),
                member.getEmail(),
                member.isDel(),
                false,
                member.getRoleSet().stream().map(memberRole -> new SimpleGrantedAuthority("ROLE_"
                        + memberRole.name())).collect(Collectors.toList())
        );

        log.info("memberSecurityDTO");
        log.info(memberSecurityDTO);

        return memberSecurityDTO;
    }
    }
