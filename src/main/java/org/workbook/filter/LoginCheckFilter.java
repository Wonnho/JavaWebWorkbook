package org.workbook.filter;

import lombok.extern.log4j.Log4j2;
import org.workbook.dto.MemberDTO;
import org.workbook.service.MemberService;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;

@WebFilter(urlPatterns = {"/todo/*"})
@Log4j2
public class LoginCheckFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res,
                         FilterChain chain)
        throws IOException, ServletException {
        log.info("login check Filter.....");

        HttpServletRequest hreq=(HttpServletRequest)req;
        HttpServletResponse hres=(HttpServletResponse)res;

        HttpSession session= hreq.getSession();

        if (session.getAttribute("loginInfo")==null) {
            hres.sendRedirect("/login");
            return;
        }

        //when loginInfo are there at session then check cookie
        Cookie cookie=findCookie(hreq.getCookies(),"remember-me");

        // login if there is no session nor cookie
        if(cookie == null) {
            hres.sendRedirect("/login");
            return;
        }

        // in case cookie exists
        log.info("cookie exists");
        //uuid
        String uuid=cookie.getValue();

        try {
            //check DB
            MemberDTO memberDTO= MemberService.INSTANCE.getByUUID(uuid);
            log.info("user info indentified by cookie value" + memberDTO);

            if (memberDTO==null) {
                throw new Exception("Cookie value is not valid");
            }

            // add user info to session
            session.setAttribute("loginInfo", memberDTO);
            chain.doFilter(req,res);

        } catch (Exception e) {
            e.printStackTrace();
            ((HttpServletResponse) res).sendRedirect("/login");
        }
    }

    private Cookie findCookie(Cookie[] cookies,String name ) {
        if(cookies==null || cookies.length==0) {
            return  null;
        }

        Optional<Cookie> result= Arrays.stream(cookies)
                .filter(ck -> ck.getName().equals(name))
                .findFirst();
        return result.isPresent()?result.get():null;
    }
}
