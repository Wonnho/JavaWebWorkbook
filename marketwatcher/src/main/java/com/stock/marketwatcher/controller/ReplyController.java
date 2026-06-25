package com.stock.marketwatcher.controller;

import com.stock.marketwatcher.dto.ReplyDTO;
import com.stock.marketwatcher.service.ReplyService;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindException;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@Log4j2
@RequestMapping("/replies")
@RequiredArgsConstructor
public class ReplyController {

    private final ReplyService replyService;

    @Operation(summary="Replies POST",description="make a comment as POST method")
    @PostMapping(value="/",consumes = MediaType.APPLICATION_JSON_VALUE)
    public Map<String, Long> register(@Valid  @RequestBody ReplyDTO replyDTO,
                                                      BindingResult bindingResult) throws BindException {
        log.info(replyDTO);

        if(bindingResult.hasErrors()) {
            throw new BindException(bindingResult);
        }

     Map<String,Long>   resultMap=new HashMap<>();
        Long rno=replyService.register(replyDTO);
        resultMap.put("rno",111L);

        return resultMap;
    }
}
