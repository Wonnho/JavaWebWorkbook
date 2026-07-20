package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.domain.Reply;
import jakarta.transaction.Transactional;
import lombok.extern.log4j.Log4j2;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;


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
                .replyText("exclude='board',룰 주석처리하고 실행하니 에러가 발생.그래서 이번에 @Transactional을 붙이니 에러가 발생하지 않음")
                .replyer("감놔라")
                .build();

       replyRepository.save(reply);
    }
    @Transactional
    @Test
    public void BoardRepliesTest() {
        Long bno=99L;
        Pageable pageable =PageRequest.of(0,10, Sort.by("rno").descending());
        Page<Reply> result=replyRepository.listOfBoard(bno,pageable);

      result.getContent().forEach(reply -> {
          log.info(reply);
      });
    }
}
