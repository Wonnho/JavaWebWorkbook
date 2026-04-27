package org.workbook;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

// Added leading slash to "cat"
@WebServlet(name="CatServlet", urlPatterns = "/cat")
public class CatServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        // Fixed the body tag syntax
        out.println("<html><body>");
        out.println("<h1>CatServlet</h1>");
        out.println("</body></html>");
    }
}