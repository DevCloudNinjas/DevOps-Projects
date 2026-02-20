package com.project.staragile.insureme;

import javax.annotation.Generated;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class Policy {
	
	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private int policyId;
	
	private String policyHolderName;
	
	private String policyType;
	
	private double policyPrice;
	
	private String policyStartDate;
	
	private String policyEndDate;
	
	

	public Policy() {
		super();
		// TODO Auto-generated constructor stub
	}

	public Policy(int policyId, String policyHolderName, String policyType, double policyPrice, String policyStartDate,
			String policyEndDate) {
		super();
		this.policyId = policyId;
		this.policyHolderName = policyHolderName;
		this.policyType = policyType;
		this.policyPrice = policyPrice;
		this.policyStartDate = policyStartDate;
		this.policyEndDate = policyEndDate;
	}

	public int getPolicyId() {
		return policyId;
	}

	public void setPolicyId(int policyId) {
		this.policyId = policyId;
	}

	public String getPolicyHolderName() {
		return policyHolderName;
	}

	public void setPolicyHolderName(String policyHolderName) {
		this.policyHolderName = policyHolderName;
	}

	public String getPolicyType() {
		return policyType;
	}

	public void setPolicyType(String policyType) {
		this.policyType = policyType;
	}

	public double getPolicyPrice() {
		return policyPrice;
	}

	public void setPolicyPrice(double policyPrice) {
		this.policyPrice = policyPrice;
	}

	public String getPolicyStartDate() {
		return policyStartDate;
	}

	public void setPolicyStartDate(String policyStartDate) {
		this.policyStartDate = policyStartDate;
	}

	public String getPolicyEndDate() {
		return policyEndDate;
	}

	public void setPolicyEndDate(String policyEndDate) {
		this.policyEndDate = policyEndDate;
	}
	
	

}
