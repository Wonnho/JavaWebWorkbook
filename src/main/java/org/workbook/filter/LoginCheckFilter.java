package org.workbook.filter;

import lombok.extern.log4j.Log4j2;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

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

        if (session.getAttribute("LoginInfo")==null) {
            hres.sendRedirect("/login");
            return;
        }

        chain.doFilter(req,res);
    }
}
