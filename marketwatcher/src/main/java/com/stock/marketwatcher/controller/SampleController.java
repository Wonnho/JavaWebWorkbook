package com.stock.marketwatcher.controller;

import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@Log4j2
public class SampleController {

    @GetMapping("/springboot")
    public void springboot(Model model) {
        log.info("Hey Guys, Welcome to Spring Boot World.........................");
        model.addAttribute("message","Hey Guys, Welcome to Spring Boot World");
    }
}
