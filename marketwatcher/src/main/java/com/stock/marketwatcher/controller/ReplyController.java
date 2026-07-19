package com.stock.marketwatcher.controller;

import com.stock.marketwatcher.dto.PageRequestDTO;
import com.stock.marketwatcher.dto.PageResponseDTO;
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
import org.springframework.web.bind.annotation.*;

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

    @Operation(summary="Replies of Board",description="retrieve a reply of a list using GET method")
    @GetMapping(value="/list/{bno}")
    public PageResponseDTO<ReplyDTO> getList(@PathVariable("bno") Long bno, PageRequestDTO pageRequestDTO) {

        PageResponseDTO<ReplyDTO> responseDTO=replyService.getListOfBoard(bno,pageRequestDTO);
        return responseDTO;

    }
    @Operation(summary = "REad Reply",description = "retrieve a reply using GET method")
    @GetMapping("/{rno}")
    public ReplyDTO getReplyDTO(@PathVariable("rno") Long rno) {
       ReplyDTO replyDTO=replyService.read(rno);
        return replyDTO;
    }

    @Operation(summary="Delete Reply",description="delete reply using DELETE method")
    @DeleteMapping("/{rno}")
    public Map<String,Long> remove(@PathVariable("rno") Long rno) {
        replyService.remove(rno);
        Map<String,Long> resultMap=new HashMap<>();
        resultMap.put("rno",rno);
        return  resultMap;
    }

    @Operation(summary = "Modify a reply",description = "modify a reply using PUT")
    @PutMapping(value="/{rno}",consumes = MediaType.APPLICATION_JSON_VALUE)
    public Map<String,Long> remove(@PathVariable("rno") Long rno,@RequestBody ReplyDTO replyDTO) {
        replyDTO.setRno(rno);
        replyService.modify(replyDTO);
        Map<String,Long> resultMap=new HashMap<>();
        resultMap.put("rno",rno);
        return  resultMap;
    }
}


