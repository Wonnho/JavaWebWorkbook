package com.stock.marketwatcher;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class MarketwatcherApplication {

	public static void main(String[] args) {
		SpringApplication.run(MarketwatcherApplication.class, args);
	}

}
