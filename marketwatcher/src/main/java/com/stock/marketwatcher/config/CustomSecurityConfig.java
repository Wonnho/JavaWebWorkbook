package com.stock.marketwatcher.config;

import com.stock.marketwatcher.security.Custom403Handler;
import com.stock.marketwatcher.security.CustomUserDetailsService;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.boot.autoconfigure.security.servlet.PathRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.security.web.authentication.rememberme.JdbcTokenRepositoryImpl;
import org.springframework.security.web.authentication.rememberme.PersistentTokenRepository;

import javax.sql.DataSource;

@Log4j2
@Configuration
//@EnableGlobalAuthentication
@EnableGlobalMethodSecurity(prePostEnabled = true)
@RequiredArgsConstructor
public class CustomSecurityConfig {

    private final DataSource dataSource;
    private final CustomUserDetailsService customerUserDetailsService;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }


    @Bean
    public SecurityFilterChain filterChain(
            HttpSecurity http) throws Exception {

        log.info("=======configure----------------");

        http.formLogin(form->form.loginPage("/member/login"));

        http.csrf(csrf -> csrf.disable());

        http.rememberMe(remember->remember
                .key("12345678")
                .tokenRepository(persistentTokenRepository())
                .userDetailsService(customerUserDetailsService)
                .tokenValiditySeconds(60*60*24*30)
        );

        http.exceptionHandling(exception -> exception
                .accessDeniedHandler(accessDeniedHandler())
        );


//        http.authorizeHttpRequests(auth -> auth
//                .requestMatchers("/member/login").permitAll()
//                .requestMatchers("/board/register").authenticated()
//                .anyRequest().permitAll()
//        );



        return http.build();
    }

    @Bean
    public AccessDeniedHandler accessDeniedHandler() {
        return new Custom403Handler();
    }

    @Bean
    public WebSecurityCustomizer webSecurityCustomizer() {
        log.info("=========web configure------------------");
        return (web) -> web.ignoring().requestMatchers(PathRequest.toStaticResources().atCommonLocations());

    }


    @Bean
   public  PersistentTokenRepository persistentTokenRepository() {
      JdbcTokenRepositoryImpl  repo=new JdbcTokenRepositoryImpl();
      repo.setDataSource(dataSource);
      return repo;
    }


}
