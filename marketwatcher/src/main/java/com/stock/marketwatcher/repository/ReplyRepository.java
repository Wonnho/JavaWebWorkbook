package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Reply;
import org.springframework.data.domain.Page;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.domain.Pageable;
//import java.awt.print.Pageable;

public interface ReplyRepository extends JpaRepository<Reply,Long> {
    @Query("select r from Reply r where r.board.bno=:bno")
    Page<Reply> ListOfBoard(Long bno, Pageable pageable);
}
