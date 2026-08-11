package com.stock.marketwatcher.dto;

import lombok.Data;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class BoardListReplyCountDTO {
    private Long bno;
    private String title;

    private String writer;

    private LocalDateTime regDate;

    private Long replyCount;


}
