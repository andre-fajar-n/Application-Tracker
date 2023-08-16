class GetPaginationRequest:
    def validate_integer(self, num, default_num=10):
        try:
            int(num)
        except ValueError:
            num = default_num
        
        return num

    def get_page(self, request):
        page = request.GET.get("page", 1)
        if page:
            return page
        
        return self.validate_integer(self, 1)
    
    def get_per_page(self, request):
        page = request.GET.get("per_page", 10)
        if page:
            return page
        
        return self.validate_integer(self, 10)