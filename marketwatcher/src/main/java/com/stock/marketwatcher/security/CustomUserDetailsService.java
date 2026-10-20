package com.stock.marketwatcher.security;

import lombok.extern.log4j.Log4j2;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Log4j2
@Service
public class CustomUserDetailsService implements UserDetailsService {

    private static final String DEMO_USERNAME = "user10";
    private static final String DEMO_PASSWORD = "4321";

    private final String encodedPassword;

    public CustomUserDetailsService() {
        PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
        this.encodedPassword = passwordEncoder.encode(DEMO_PASSWORD);
    }

    @Override
    public UserDetails loadUserByUsername(String username)
            throws UsernameNotFoundException {

        log.info("loadUserByUsername: {}", username);

        if (!DEMO_USERNAME.equals(username)) {
            throw new UsernameNotFoundException(
                    "User not found: " + username);
        }

        return User.builder()
                .username(DEMO_USERNAME)
                .password(encodedPassword)
                .authorities("ROLE_USER")
                .build();
    }
}
