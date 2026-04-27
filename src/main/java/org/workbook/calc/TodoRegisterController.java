package org.workbook.calc;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import javax.servlet.annotation.WebServlet;
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
