package com.stock.marketwatcher.service;

import com.stock.marketwatcher.dto.MemberJoinDTO;

public interface MemberService {

    void changePassword(String username, String mpw);

    static class MidExistException extends Exception {

    }

    void join(MemberJoinDTO memberJoinDTO) throws MidExistException;
}
