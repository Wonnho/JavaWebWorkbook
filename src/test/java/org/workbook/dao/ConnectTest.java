package org.workbook.dao;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class ConnectTest {

    @Test
    public void test() {
        int v1=131;
        int v2=131;
        Assertions.assertEquals(v1,v2);
    }

    @Test
    public void testConnection() throws Exception{

        Class.forName("org.mariadb.jdbc.Driver");
        Connection connection= DriverManager.getConnection(
                "jdbc:mariadb://localhost:3309/webdb",
                "webuser",
                "webuser"
        );
        Assertions.assertNotNull(connection);
        connection.close();

    }

    @Test
    public void table_check () throws Exception {
        Connection conn = DriverManager.getConnection(
                "jdbc:mariadb://localhost:3309/webdb",
                "webuser",
                "webuser"
        );
        Statement stmt = conn.createStatement();

        ResultSet rs = stmt.executeQuery("SHOW TABLES");

        while (rs.next()) {
            System.out.println(rs.getString(1));
        }

        conn.close();
    }
}
