package org.workbook.todo;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.workbook.todo.dto.TodoDTO;
import org.workbook.todo.service.TodoService;

import java.io.IOException;
import java.util.List;

@WebServlet(name="listController",urlPatterns = "/todo/list")
public class TodoListController extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req,HttpServletResponse res) throws
            ServletException, IOException {
          System.out.println("/todo/list");
            List<TodoDTO> dtoList= TodoService.INSTANCE.getList();
            req.setAttribute("list",dtoList);
          req.getRequestDispatcher("/WEB-INF/todo/list.jsp").forward(req,res);
        }
}
