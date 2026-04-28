package org.workbook.dao;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
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

    @Test
    public void hikariCPconnectionTest() throws Exception {
        HikariConfig config=new HikariConfig();
        config.setDriverClassName("org.mariadb.jdbc.Driver");
        config.setJdbcUrl("jdbc:mariadb://localhost:3309/webdb");
        config.setUsername("webuser");
        config.setPassword("webuser");
        config.addDataSourceProperty("cachePrepStmts","true");
        config.addDataSourceProperty("prepStmtCacheSize","250");
        config.addDataSourceProperty("prepStmtCacheSqlLimit","2048");

        HikariDataSource ds=new HikariDataSource(config);
        Connection connection=ds.getConnection();
        System.out.println(connection);
        connection.close();


    }
}
