package org.workbook.dao;

import lombok.Cleanup;
import org.workbook.domain.MemberVO;

import java.sql.Connection;

import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class MemberDAO {
    public MemberVO getWithPassword(String todoid, String todopw) throws Exception {


        String query = "SELECT todoid,todopw,todoname FROM tbl_member WHERE todoid=? AND todopw=?";

        MemberVO memberVO=null;

        @Cleanup Connection conn = ConnectionUtil.INSTANCE.getConnection(); // 네가 만든 커넥션 유틸
        @Cleanup PreparedStatement ps = conn.prepareStatement(query);
        ps.setString(1, todoid);
        ps.setString(2, todopw);

        @Cleanup ResultSet rs = ps.executeQuery();

         rs.next(); // 있으면 true (로그인 성공)

        memberVO= MemberVO.builder()
                .todoid(rs.getString(1))
                .todopw(rs.getString(2))
                .todoname(rs.getString(3))
                .build();

                return memberVO;
    }
}
