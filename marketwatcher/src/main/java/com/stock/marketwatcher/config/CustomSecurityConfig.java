package com.stock.marketwatcher.config;

import com.stock.marketwatcher.security.CustomerUserDetailsService;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.security.servlet.PathRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.configuration.EnableGlobalAuthentication;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
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
    private final CustomerUserDetailsService customerUserDetailsService;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception{
        log.info("=======configure----------------");

        http.csrf(csrf -> csrf.disable());

        http.rememberMe(remember->remember
                .key("12345678")
                .tokenRepository(persistentTokenRepository())
                .userDetailsService(customerUserDetailsService)
                .tokenValiditySeconds(60*60*24*30)
        );



        http.authorizeHttpRequests(auth -> auth
                .requestMatchers("/member/login").permitAll()
                .requestMatchers("/board/register").authenticated()
                .anyRequest().permitAll()
        );

        http.formLogin(form->form.loginPage("/member/login"));
//                .defaultSuccessUrl("/member/register", true));

        return http.build();
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
