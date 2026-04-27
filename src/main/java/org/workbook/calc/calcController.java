package org.workbook.calc;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet(name = "calcController", urlPatterns = "/calculator/makeResult")
public class calcController extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws

            ServletException, IOException {

        String num1=req.getParameter("num1");
        String num2=req.getParameter("num2");
        System.out.printf("num1: %s",num1);
        System.out.printf("num1: %s",num2);
        System.out.printf("sum: %s",num1+num2);

        res.sendRedirect("/index");



    }
}
