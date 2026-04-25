package org.workbook.sample; // Adjust to your actual package name

// ====== NEW IMPORTS (Crucial for fixing the errors) ======
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
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