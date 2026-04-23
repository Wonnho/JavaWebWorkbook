package org.workbook;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
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