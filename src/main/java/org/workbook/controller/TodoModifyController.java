package org.workbook.controller;

import lombok.extern.log4j.Log4j2;
import org.workbook.dto.TodoDTO;
import org.workbook.service.TodoService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.sql.rowset.serial.SerialException;
import java.io.IOException;
import java.time.format.DateTimeFormatter;

@WebServlet(name="todoModifyController",value="/todo/modify")
@Log4j2
public class TodoModifyController extends HttpServlet {

    private TodoService todoService=TodoService.INSTANCE;
    private final DateTimeFormatter DATAFORMATTER=
            DateTimeFormatter.ofPattern("yyyy-MM-dd");

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws
            ServletException, IOException {
        try {

            Long tno=Long.parseLong(req.getParameter("tno"));
            TodoDTO todoDTO=todoService.get(tno);
            req.setAttribute("dto",todoDTO);
            req.getRequestDispatcher("/WEB-INF/todo/modify.jsp").forward(req,res);
        } catch (Exception e) {
            log.error(e.getMessage());
            throw new ServletException("modify get....error");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req,HttpServletResponse res)
        throws ServletException, IOException{

        String finishedSTr=req.getParameter("done");


    }
}
