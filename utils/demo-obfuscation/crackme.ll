; ModuleID = 'crackme.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-redhat-linux-gnu"

%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct._IO_FILE*, i32 }

@passwd = global [8 x i8] c"\1B\04\15\02\5C\18\00\00", align 1
@.str = private unnamed_addr constant [5 x i8] c"/tmp\00", align 1
@.str1 = private unnamed_addr constant [2 x i8] c"r\00", align 1
@.str2 = private unnamed_addr constant [37 x i8] c"I'm sorry GDB! You are not allowed!\0A\00", align 1
@.str3 = private unnamed_addr constant [31 x i8] c"Tracing is not allowed... Bye\0A\00", align 1
@.str4 = private unnamed_addr constant [29 x i8] c"Please tell me my password: \00", align 1
@stdout = external global %struct._IO_FILE*
@stdin = external global %struct._IO_FILE*
@.str5 = private unnamed_addr constant [45 x i8] c"The password is correct!\0ACongratulations!!!\0A\00", align 1
@.str6 = private unnamed_addr constant [28 x i8] c"No! No! No! No! Try again.\0A\00", align 1
@llvm.global_ctors = appending global [1 x { i32, void ()*, i8* }] [{ i32, void ()*, i8* } { i32 65535, void ()* @detect_gdb, i8* null }]

; Function Attrs: nounwind uwtable
define void @detect_gdb() #0 {
  %fd = alloca %struct._IO_FILE*, align 8
  %1 = call %struct._IO_FILE* @fopen(i8* getelementptr inbounds ([5 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([2 x i8]* @.str1, i32 0, i32 0))
  store %struct._IO_FILE* %1, %struct._IO_FILE** %fd, align 8
  %2 = load %struct._IO_FILE** %fd, align 8
  %3 = call i32 @fileno(%struct._IO_FILE* %2) #4
  %4 = icmp sgt i32 %3, 5
  br i1 %4, label %5, label %7

; <label>:5                                       ; preds = %0
  %6 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([37 x i8]* @.str2, i32 0, i32 0))
  call void @exit(i32 1) #5
  unreachable

; <label>:7                                       ; preds = %0
  %8 = load %struct._IO_FILE** %fd, align 8
  %9 = call i32 @fclose(%struct._IO_FILE* %8)
  %10 = call i64 (i32, ...)* @ptrace(i32 0, i32 0, i32 1, i32 0) #4
  %11 = icmp slt i64 %10, 0
  br i1 %11, label %12, label %14

; <label>:12                                      ; preds = %7
  %13 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([31 x i8]* @.str3, i32 0, i32 0))
  call void @exit(i32 1) #5
  unreachable

; <label>:14                                      ; preds = %7
  ret void
}

declare %struct._IO_FILE* @fopen(i8*, i8*) #1

; Function Attrs: nounwind
declare i32 @fileno(%struct._IO_FILE*) #2

declare i32 @printf(i8*, ...) #1

; Function Attrs: noreturn nounwind
declare void @exit(i32) #3

declare i32 @fclose(%struct._IO_FILE*) #1

; Function Attrs: nounwind
declare i64 @ptrace(i32, ...) #2

; Function Attrs: nounwind uwtable
define void @xor(i8* %p) #0 {
  %1 = alloca i8*, align 8
  %i = alloca i32, align 4
  store i8* %p, i8** %1, align 8
  store i32 0, i32* %i, align 4
  br label %2

; <label>:2                                       ; preds = %14, %0
  %3 = load i32* %i, align 4
  %4 = icmp slt i32 %3, 6
  br i1 %4, label %5, label %17

; <label>:5                                       ; preds = %2
  %6 = load i32* %i, align 4
  %7 = sext i32 %6 to i64
  %8 = load i8** %1, align 8
  %9 = getelementptr inbounds i8* %8, i64 %7
  %10 = load i8* %9, align 1
  %11 = sext i8 %10 to i32
  %12 = xor i32 %11, 108
  %13 = trunc i32 %12 to i8
  store i8 %13, i8* %9, align 1
  br label %14

; <label>:14                                      ; preds = %5
  %15 = load i32* %i, align 4
  %16 = add nsw i32 %15, 1
  store i32 %16, i32* %i, align 4
  br label %2

; <label>:17                                      ; preds = %2
  ret void
}

; Function Attrs: nounwind uwtable
define i32 @compare(i8* %input, i8* %passwd) #0 {
  %1 = alloca i32, align 4
  %2 = alloca i8*, align 8
  %3 = alloca i8*, align 8
  store i8* %input, i8** %2, align 8
  store i8* %passwd, i8** %3, align 8
  br label %4

; <label>:4                                       ; preds = %23, %0
  %5 = load i8** %2, align 8
  %6 = load i8* %5, align 1
  %7 = sext i8 %6 to i32
  %8 = load i8** %3, align 8
  %9 = load i8* %8, align 1
  %10 = sext i8 %9 to i32
  %11 = icmp eq i32 %7, %10
  br i1 %11, label %12, label %28

; <label>:12                                      ; preds = %4
  %13 = load i8** %2, align 8
  %14 = load i8* %13, align 1
  %15 = sext i8 %14 to i32
  %16 = icmp eq i32 %15, 0
  br i1 %16, label %22, label %17

; <label>:17                                      ; preds = %12
  %18 = load i8** %3, align 8
  %19 = load i8* %18, align 1
  %20 = sext i8 %19 to i32
  %21 = icmp eq i32 %20, 0
  br i1 %21, label %22, label %23

; <label>:22                                      ; preds = %17, %12
  br label %28

; <label>:23                                      ; preds = %17
  %24 = load i8** %2, align 8
  %25 = getelementptr inbounds i8* %24, i32 1
  store i8* %25, i8** %2, align 8
  %26 = load i8** %3, align 8
  %27 = getelementptr inbounds i8* %26, i32 1
  store i8* %27, i8** %3, align 8
  br label %4

; <label>:28                                      ; preds = %22, %4
  %29 = load i8** %2, align 8
  %30 = load i8* %29, align 1
  %31 = sext i8 %30 to i32
  %32 = icmp eq i32 %31, 0
  br i1 %32, label %33, label %39

; <label>:33                                      ; preds = %28
  %34 = load i8** %3, align 8
  %35 = load i8* %34, align 1
  %36 = sext i8 %35 to i32
  %37 = icmp eq i32 %36, 0
  br i1 %37, label %38, label %39

; <label>:38                                      ; preds = %33
  store i32 0, i32* %1
  br label %40

; <label>:39                                      ; preds = %33, %28
  store i32 -1, i32* %1
  br label %40

; <label>:40                                      ; preds = %39, %38
  %41 = load i32* %1
  ret i32 %41
}

; Function Attrs: nounwind uwtable
define i32 @main() #0 {
  %1 = alloca i32, align 4
  %input = alloca [8 x i8], align 1
  store i32 0, i32* %1
  %2 = load %struct._IO_FILE** @stdout, align 8
  %3 = call i32 @fputs(i8* getelementptr inbounds ([29 x i8]* @.str4, i32 0, i32 0), %struct._IO_FILE* %2)
  %4 = getelementptr inbounds [8 x i8]* %input, i32 0, i32 0
  %5 = load %struct._IO_FILE** @stdin, align 8
  %6 = call i8* @fgets(i8* %4, i32 7, %struct._IO_FILE* %5)
  %7 = getelementptr inbounds [8 x i8]* %input, i32 0, i32 0
  call void @xor(i8* %7)
  %8 = getelementptr inbounds [8 x i8]* %input, i32 0, i32 0
  %9 = call i32 @compare(i8* %8, i8* getelementptr inbounds ([8 x i8]* @passwd, i32 0, i32 0))
  %10 = icmp eq i32 %9, 0
  br i1 %10, label %11, label %14

; <label>:11                                      ; preds = %0
  %12 = load %struct._IO_FILE** @stdout, align 8
  %13 = call i32 @fputs(i8* getelementptr inbounds ([45 x i8]* @.str5, i32 0, i32 0), %struct._IO_FILE* %12)
  br label %17

; <label>:14                                      ; preds = %0
  %15 = load %struct._IO_FILE** @stdout, align 8
  %16 = call i32 @fputs(i8* getelementptr inbounds ([28 x i8]* @.str6, i32 0, i32 0), %struct._IO_FILE* %15)
  br label %17

; <label>:17                                      ; preds = %14, %11
  ret i32 0
}

declare i32 @fputs(i8*, %struct._IO_FILE*) #1

declare i8* @fgets(i8*, i32, %struct._IO_FILE*) #1

attributes #0 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nounwind }
attributes #5 = { noreturn nounwind }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"clang version 3.5.0 (tags/RELEASE_350/final)"}
