package com.screen;

public class Result {
	private int fieldsCount;
	private int totalRowsCount;

	public Result(int fieldsCount, int totalRowsCount) {
		this.fieldsCount = fieldsCount;
		this.totalRowsCount = totalRowsCount;
	}

	public int getFieldsCount() {
		return fieldsCount;
	}

	public int getTotalRowsCount() {
		return totalRowsCount;
	}

}
