package com.project.staragile.insureme;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PolicyController {
	
	@Autowired
	PolicyService policyService;
	
	
	@GetMapping("/hello")
	public String sayHello() {
		return "hello";
	}
	
	@GetMapping("/createPolicy")
	public Policy createPolicy() {
		
		return policyService.CreatePolicy();
		
		
	}
	
	@PostMapping("/createPolicy")
	public Policy createPolicy(@RequestBody Policy policy) {
		if(policy!=null) {
			return policyService.registerPolicy(policy);
		}
		return null;
	}

	@GetMapping("/getPolicy/{policyId}")
	public Policy getPolicyDetails(@PathVariable(value="policyId") int policyId) {
		return policyService.getPolicyDetails(policyId);
	}
	
}

