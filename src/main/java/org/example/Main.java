package org.example;

import java.sql.*;

public class Main {
    public static void main(String[] args) {
        String url = "jdbc:mariadb://localhost:3309/webdb";
        String user = "webuser";
        String password = "webuser";

        try (Connection conn = DriverManager.getConnection(url, user, password)) {
            System.out.println("DB 연결 성공!");

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT 1");

            while (rs.next()) {
                System.out.println(rs.getInt(1));
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}