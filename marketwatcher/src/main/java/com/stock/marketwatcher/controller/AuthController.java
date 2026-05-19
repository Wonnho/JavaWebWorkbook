package com.stock.marketwatcher.controller;

import com.stock.marketwatcher.domain.User;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;

@RequiredArgsConstructor
public class AuthController {
    private final User user;

    @GetMapping("/signup")
    public void signup() {


    }
}
