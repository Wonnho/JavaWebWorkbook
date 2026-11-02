package com.stock.marketwatcher.controller;

import com.stock.marketwatcher.dto.MemberJoinDTO;
import com.stock.marketwatcher.dto.MemberSecurityDTO;
import com.stock.marketwatcher.service.MemberService;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@Log4j2
@RequiredArgsConstructor
@RequestMapping("/member")
public class MemberController {

    private final MemberService memberService;

    @GetMapping("/login")
    public void LoginGET(String errorCode,String logout) {
        log.info("login get ......................");
        log.info("Logout: " +  logout);

        if(logout !=null) {
            log.info("user logout.....");
        }
//        return "member/login";
    }

    @GetMapping("/join")
    public void joinGET() {

        log.info("join get....");
    }

    @PostMapping("/join")
    public String joinPOST(MemberJoinDTO memberJoinDTO, RedirectAttributes redirectAttributes) {
        log.info("join post...");
        log.info(memberJoinDTO);

try {
    memberService.join(memberJoinDTO);

} catch (MemberService.MidExistException e) {
    redirectAttributes.addFlashAttribute("error","mid");
    return "redirect:/member/join";
}
   redirectAttributes.addFlashAttribute("result","success");
        return "redirect:/member/login";
    }

    @GetMapping("/modify")
    public String modifyGET() {
        return "member/modify";
    }

    @PostMapping("/modify")
    public String modifyPOST(
            @AuthenticationPrincipal MemberSecurityDTO principal,
            String mpw) {

        memberService.changePassword(principal.getUsername(), mpw);

        return "redirect:/board/list";
    }

}
