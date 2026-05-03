package org.workbook.controller;

import lombok.extern.log4j.Log4j2;
import org.workbook.dto.TodoDTO;
import org.workbook.service.TodoService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet(name="todoReadController", value="/todo/read")
@Log4j2
public class TodoReadController extends HttpServlet {

    private TodoService todoService=TodoService.INSTANCE;

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        try {
         Long tno=Long.parseLong(req.getParameter("tno"));
            TodoDTO todoDTO=todoService.get(tno);

            //contain model
            req.setAttribute("dto",todoDTO);

            //search Cookie
            Cookie viewTodoCookie=findCookie(req.getCookies(),"viewTodos");
            String todoListstr=viewTodoCookie.getValue();
            boolean exist=false;

            if(todoListstr !=null && todoListstr.indexOf(tno+"-")>=0) {
                exist=true;
            }

            log.info("exist:" + exist);

            if(exist) {
                todoListstr +=tno+"-";
                viewTodoCookie.setValue(todoListstr);
                viewTodoCookie.setMaxAge(60*60*24);
                viewTodoCookie.setPath("/");
                res.addCookie(viewTodoCookie);
            }


            req.getRequestDispatcher("/WEB-INF/todo/read.jsp").forward(req,res);
        } catch (Exception e) {
          log.error(e.getMessage());
          throw new ServletException("read error");
        }


    }

    private Cookie findCookie(Cookie[] cookies, String cookieName) {
        Cookie targetCookie=null;
        if(cookies !=null && cookies.length>0) {
            for(Cookie ck:cookies) {
                if(ck.getName().equals(cookieName)) {
                    targetCookie=ck;
                    break;
                }
            }
        }
        if(targetCookie==null) {
            targetCookie=new Cookie(cookieName,"");
            targetCookie.setPath("/");
            targetCookie.setMaxAge(60*60*24);
        }
        return targetCookie;
    }
}
