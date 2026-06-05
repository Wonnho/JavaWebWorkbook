package com.stock.marketwatcher.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI marketWatcherOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Boot 01 Project Swagger") // Replaces .apiInfo(apiInfo())
                        .version("v1.0.0"));
    }

    @Bean
    public GroupedOpenApi publicApi() {
        return GroupedOpenApi.builder()
                .group("boot01-public")
                // Replaces .apis(RequestHandlerSelectors.basePackage("..."))
                .packagesToScan("com.stock.marketwatcher.controller")
                // Replaces .paths(PathSelectors.any())
                .pathsToMatch("/**")
                .build();
    }
}