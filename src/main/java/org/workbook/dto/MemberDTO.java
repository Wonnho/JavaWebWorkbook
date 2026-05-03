package org.workbook.dto;


import lombok.*;

@NoArgsConstructor
@AllArgsConstructor
@Builder
@Data
@ToString
public class MemberDTO {

    private String todoid;
    private String todopw;
    private String todoname;
    private String uuid;

}
