struct Rectangle(Shape){
    public let a = 0
    private let b = 1
}

impl Rectangle(Shape){
    public func field(){
        return a + b
    }
}