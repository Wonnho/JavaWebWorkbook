package org.workbook.calc;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet(name="inputController", urlPatterns = "/calc/input")
public class inputController  extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws
            ServletException, IOException{
        System.out.println("InputController...doGet...");
        RequestDispatcher dispatcher=request.getRequestDispatcher("/WEB-INF/calculator/input.jsp");
        dispatcher.forward(request,response);
    }



}
