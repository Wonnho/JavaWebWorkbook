package com.stock.marketwatcher.domain;


import jakarta.persistence.*;
import org.springframework.security.core.GrantedAuthority;

import java.util.Collection;

@Entity
@Table(name="users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

private String username;
private String password;

private String email;

private String mobile;
private String majorKey;

}
