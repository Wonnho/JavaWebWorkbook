package com.stock.marketwatcher.domain;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name="Reply",indexes = {@Index(name="indx_reply_board_bno",columnList = "board_bno")})
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@ToString //(exclude = "board")
public class Reply extends BaseEntity{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long rno;

    private String replyText;

    private String replyer;

    @ManyToOne(fetch = FetchType.LAZY)
    private Board board;

    public void changeText(String text) {
        this.replyText=text;
    }
}
