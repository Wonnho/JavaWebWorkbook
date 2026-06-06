package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.domain.Reply;
import lombok.extern.log4j.Log4j2;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
@Log4j2
public class ReplyRepositoryTests {
    @Autowired
    private ReplyRepository replyRepository;

    @Test
    public void InsertTest() {
      Long  bno=99L;

        Board board=Board.builder().bno(bno).build();
       Reply reply= Reply.builder()
                .board(board)
                .replyText("백 번 댓글을 붙여봐")
                .replyer("감놔라")
                .build();

       replyRepository.save(reply);
    }
}
