package org.workbook.controller;

import lombok.extern.log4j.Log4j2;
import org.workbook.dto.MemberDTO;
import org.workbook.service.MemberService;

import javax.security.sasl.SaslException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

@WebServlet("/login")
@Log4j2
public class LoginController extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws SaslException, IOException, ServletException {
        log.info("Login get...............");
       req.getRequestDispatcher("/WEB-INF/login.jsp").forward(req,res);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws SaslException, IOException, ServletException {
        log.info("Login post...............");

        String todoid = req.getParameter("todoid");
        String todopw = req.getParameter("todopw");

        try {
            //  String str=todoid + todopw;
            MemberDTO memberDTO = MemberService.INSTANCE.login(todoid, todopw);
            HttpSession session = req.getSession();
            session.setAttribute("loginInfo", memberDTO);
            res.sendRedirect("/todo/list");
        } catch (Exception e) {
            res.sendRedirect("login?result=error");
        }
    }
    }
