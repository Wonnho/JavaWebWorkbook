package com.stock.marketwatcher.dto.upload;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class UploadResultDTO {

    private String uuid;
    private String fileName;
    private boolean img;

    public String getLink() {
        if(img) {
            return "s+"+ uuid +"_"+fileName;

        } else {
            return uuid+"_"+fileName;
        }
    }
}
