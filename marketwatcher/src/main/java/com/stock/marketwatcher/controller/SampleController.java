package com.stock.marketwatcher.controller;

import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

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


    class SampleDTO {
        private String p1,p2,p3;

        public String getP1() {
            return p1;
        }

        public String getP2() {
            return p2;
        }

        public String getP3() {
            return p3;
        }
    }

    @GetMapping("thymeleaf/inlinefct")
    public void inlinefct(Model model) {

        log.info("thymelieaf inline.................");
        List<String> strList=IntStream.range(1,10)
                .mapToObj(k -> "Data" + k)
                .collect(Collectors.toList());

        model.addAttribute("list",strList);

         Map<String,String> map=new HashMap<>();
         map.put("Fred Ramsdell","Sonoma");
         map.put("Elon Musk","Tesla");

         model.addAttribute("map",map);
         // compare above model.addAttribute with the last one

        SampleDTO sampleDTO=new SampleDTO();
           sampleDTO.p1="value --- p1";
            sampleDTO.p2="value --- p2";
            sampleDTO.p3="value --- p3";

            model.addAttribute("dto",sampleDTO);
    }

    @GetMapping("/thymeleaf/body/bodycontent")
    public void bodycontent(Model model) {
         model.addAttribute("fruits",new String[]{"thymeleaf","melon","peach"});

    }
}
