package com.stock.marketwatcher.dto;

import lombok.Setter;
import org.springframework.security.core.userdetails.User;
import lombok.Getter;
import org.springframework.boot.web.embedded.undertow.UndertowServletWebServer;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.core.user.OAuth2User;

import java.util.Collection;
import java.util.Map;

@Getter
@Setter
public class MemberSecurityDTO extends User implements OAuth2User {

    private String mid;
    private String mpw;
    private String email;
    private boolean del;

    private boolean social;

    private Map<String,Object> props;


    public MemberSecurityDTO(String username, String password, String email, boolean del, boolean social,
                                 Collection<? extends GrantedAuthority> authorities) {

                   super(username,password,authorities);

                   this.mid=username;
                   this.mpw=password;
                   this.email=email;
                   this.del=del;
                   this.social=social;


        }

//    @Override
//    public <A> A getAttribute(String name) {
//        return OAuth2User.super.getAttribute(name);
//    }

    @Override
    public Map<String,Object> getAttributes() {
        return this.getProps();
    }

    @Override
    public String getName() {
        return this.mid;
    }
}
