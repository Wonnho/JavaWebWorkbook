package org.workbook.sample; // Adjust to your actual package name

// ====== NEW IMPORTS (Crucial for fixing the errors) ======
import javax.servlet.ServletException;
import javax.servlet.ServletConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
// ==========================================================

@WebServlet(name="sampleServlet", urlPatterns = "/sample")
public class SampleServlet extends HttpServlet {

    // (This Override works now)
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        System.out.println("doGet..."+this);
    }

    @Override
    public void destroy() {
        System.out.println("destroy...");
    }

    // (The signature now matches)
    @Override
    public void init(ServletConfig config) throws ServletException{
        System.out.println(("initializing(ServletConfig).............."));
    }

}