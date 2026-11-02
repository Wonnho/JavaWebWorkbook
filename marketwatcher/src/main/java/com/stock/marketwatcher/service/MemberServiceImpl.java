package com.stock.marketwatcher.service;

import com.stock.marketwatcher.domain.Member;
import com.stock.marketwatcher.domain.MemberRole;
import com.stock.marketwatcher.dto.MemberJoinDTO;
import com.stock.marketwatcher.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.modelmapper.ModelMapper;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Log4j2
@Service
@RequiredArgsConstructor
public class MemberServiceImpl implements MemberService{

    private final MemberRepository memberRepository;

    private final ModelMapper modelMapper;

    private final PasswordEncoder passwordEncoder;
    @Override
    public void join(MemberJoinDTO memberJoinDTO) throws MidExistException {
     String  mid= memberJoinDTO.getMid();
           boolean  isMid=memberRepository.existsById(mid);

           if(isMid) {
               throw new MidExistException();
           }

           Member  member=modelMapper.map(memberJoinDTO, Member.class);
           member.changePassword(passwordEncoder.encode(memberJoinDTO.getMpw()));
           member.addRole(MemberRole.USER);

           log.info("----------------------------");
           log.info(member);
           log.info(member.getRoleSet());

           memberRepository.save(member);

    }
    @Override
    @Transactional
    public void changePassword(String username, String rawPassword) {

        if (rawPassword == null || rawPassword.isBlank()) {
            throw new IllegalArgumentException("Password must not be empty");
        }

        String encodedPassword = passwordEncoder.encode(rawPassword);

        int updatedRows =
                memberRepository.updatePassword(encodedPassword, username);

        if (updatedRows != 1) {
            throw new IllegalArgumentException(
                    "Member not found: " + username
            );
        }
    }
}
