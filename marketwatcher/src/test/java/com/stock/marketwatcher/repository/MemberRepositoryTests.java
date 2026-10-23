package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Member;
import com.stock.marketwatcher.domain.MemberRole;
import lombok.extern.log4j.Log4j2;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;
import java.util.stream.IntStream;

@SpringBootTest
@Log4j2
public class MemberRepositoryTests {
    @Autowired
    private MemberRepository memberRepository;
    @Autowired
    private PasswordEncoder passwordEncoder;

    @Test
    public void insertMembers() {

        IntStream.rangeClosed(1,100).forEach(k-> {
         Member member   =Member.builder()
                    .mid("member"+k)
                    .mpw(passwordEncoder.encode("4321"))
                    .email("email"+k+"@marketwatcher.com")
                    .build();
              member.addRole(MemberRole.USER);

              if(k>=90) {
                  member.addRole(MemberRole.ADMIN);
              }
              memberRepository.save(member);

        });
    }

    @Test
    public void testRead() {
        Optional<Member> members=memberRepository.getWithRoles("member100");
        Member member=members.orElseThrow();

        log.info(member);
        log.info(member.getRoleSet());
        member.getRoleSet().forEach(memberRole -> log.info(memberRole.name()));
    }
    }

