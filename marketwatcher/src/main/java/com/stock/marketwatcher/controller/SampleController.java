package com.stock.marketwatcher.controller;

import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.Arrays;
import java.util.List;

@Controller
@Log4j2
public class SampleController {

    @GetMapping("/springboot")
    public void springboot(Model model) {
        log.info("Hey Guys, Welcome to Spring Boot World.........................");
        model.addAttribute("message","Hey Guys, Welcome to Spring Boot World");
    }

    @GetMapping("/thymeleaf/jackson")
    public void jackson(Model model) {
        List<String> list=Arrays.asList("JSON","javascript on notation","jackson","databind");
        model.addAttribute("List",list);
    }

    @GetMapping("/thymeleaf/repetition")
    public void repetition(Model model) {
        List<String> list=Arrays.asList("JSON","<th:each>","<ch:block>","repetition");
        model.addAttribute("List",list);
    }
}
