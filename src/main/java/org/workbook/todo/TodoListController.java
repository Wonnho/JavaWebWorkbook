package org.workbook.todo;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet(name="listController",urlPatterns = "/todo/list")
public class TodoListController extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req,HttpServletResponse res) throws
            ServletException, IOException {
          System.out.println("/todo/list");
          req.getRequestDispatcher("/WEB-INF/todo/list.jsp").forward(req,res);
        }
}
