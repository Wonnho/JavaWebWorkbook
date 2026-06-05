package com.stock.marketwatcher.controller;

import com.stock.marketwatcher.dto.ReplyDTO;
import io.swagger.v3.oas.annotations.Operation;
import lombok.extern.log4j.Log4j2;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@Log4j2
@RequestMapping("/replies")
public class ReplyController {

    @Operation(summary="Replies POST",description="make a comment as POST method")
    @PostMapping(value="/",consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, Long>> register(@RequestBody ReplyDTO replyDTO) {
        log.info(replyDTO);
     Map<String,Long>   resultMap=Map.of("rno",111L);
        return ResponseEntity.ok(resultMap);
    }
}
