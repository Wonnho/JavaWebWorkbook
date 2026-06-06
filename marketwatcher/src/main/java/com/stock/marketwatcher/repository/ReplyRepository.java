package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Reply;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ReplyRepository extends JpaRepository<Reply,Long> {
}
