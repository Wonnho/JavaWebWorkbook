package org.workbook.calc;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import jakarta.servlet.annotation.WebServlet;
import java.io.IOException;

@WebServlet(name="todoRegisterController",urlPatterns = "/todo/register")
public class TodoRegisterController extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws
            ServletException, IOException{

        System.out.println(" Screen of input");

        RequestDispatcher dispatcher=req.getRequestDispatcher("/WEB-INF/todo/register.jsp");
            dispatcher.forward(req,res);
    }



    @Override
    protected void doPost(HttpServletRequest req,HttpServletResponse res) throws
            ServletException, IOException{

        System.out.println(" process data and move to list");

        res.sendRedirect("/todo/list");
    }


}
