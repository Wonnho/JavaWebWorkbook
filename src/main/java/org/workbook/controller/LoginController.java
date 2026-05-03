package org.workbook.controller;

import lombok.extern.log4j.Log4j2;
import org.workbook.dto.MemberDTO;
import org.workbook.service.MemberService;

import javax.security.sasl.SaslException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.util.UUID;

@WebServlet("/login")
@Log4j2
public class LoginController extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws SaslException, IOException, ServletException {
        log.info("Login get...............");
        req.getRequestDispatcher("/WEB-INF/login.jsp").forward(req, res);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws SaslException, IOException, ServletException {
        log.info("Login post...............");

        String todoid = req.getParameter("todoid");
        String todopw = req.getParameter("todopw");

        String auto = req.getParameter("auto");
        boolean rememberMe = auto != null && auto.equals("on");


        try {
            //  String str=todoid + todopw;
            MemberDTO memberDTO = MemberService.INSTANCE.login(todoid, todopw);

            if (rememberMe) {
                String uuid = UUID.randomUUID().toString();
                MemberService.INSTANCE.updateUuid(todoid,uuid);
                memberDTO.setUuid(uuid);

                Cookie rememberCookie=new Cookie("remember-me",uuid);
                rememberCookie.setMaxAge(60*60*24*7);
                rememberCookie.setPath("/");

                res.addCookie(rememberCookie);
            }

            HttpSession session = req.getSession();
            session.setAttribute("loginInfo", memberDTO);
            res.sendRedirect("/todo/list");
        } catch (Exception e) {
            res.sendRedirect("login?result=error");
        }
    }

    }
