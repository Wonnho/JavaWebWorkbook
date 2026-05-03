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

    public void updateUuid(String todoid,String uuid) throws Exception {
        String sql="update tbl_member set uuid=? where todoid=?";
        @Cleanup Connection conn = ConnectionUtil.INSTANCE.getConnection(); // 네가 만든 커넥션 유틸
        @Cleanup PreparedStatement ps = conn.prepareStatement(sql);

        ps.setString(1,uuid);
        ps.setString(2,todoid);
        ps.executeUpdate();

    }

    public MemberVO selectUUID(String uuid) throws Exception {
        String sql="select todoid, todopw, todoname,uuid from tbl_member where uuid=?";

        @Cleanup Connection conn = ConnectionUtil.INSTANCE.getConnection(); // 네가 만든 커넥션 유틸
        @Cleanup PreparedStatement ps = conn.prepareStatement(sql);

        ps.setString(1,uuid);

        @Cleanup ResultSet rs=ps.executeQuery();

        rs.next(); // 있으면 true (로그인 성공)

        MemberVO memberVO= MemberVO.builder()
                .todoid(rs.getString(1))
                .todopw(rs.getString(2))
                .todoname(rs.getString(3))
                .uuid(rs.getString(4))
                .build();

        return memberVO;

    }
}
