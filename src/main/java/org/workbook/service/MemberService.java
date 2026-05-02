package org.workbook.service;

import org.modelmapper.ModelMapper;
import org.workbook.dao.MemberDAO;
import org.workbook.domain.MemberVO;
import org.workbook.dto.MemberDTO;
import org.workbook.util.MapperUtil;

public enum MemberService {
    INSTANCE;
    private MemberDAO dao;
    private ModelMapper modelMapper;

    MemberService() {
        dao=new MemberDAO();
        modelMapper= MapperUtil.INSTANCE.get();
    }

    public MemberDTO login(String todoid,String todopw) throws Exception {
        MemberVO vo=dao.getWithPassword(todoid,todopw);
        MemberDTO memberDTO=modelMapper.map(vo, MemberDTO.class);
        return  memberDTO;
    }
}
