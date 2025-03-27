import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function InsuranceForm() {
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    dob: "",
    email: "",
    phone: "",
    insuranceType: ""
  });

  const getInsuranceType = (age) => {
    if (age < 18) return "No insurance available";
    if (age >= 18 && age < 30) return "Health Insurance, Car Insurance";
    if (age >= 30 && age < 50) return "Life Insurance, Home Insurance";
    return "Senior Citizen Insurance, Life Insurance";
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const insurance = getInsuranceType(parseInt(formData.age));
    setFormData((prev) => ({ ...prev, insuranceType: insurance }));
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <Card className="p-6 w-96 shadow-lg bg-white rounded-2xl">
        <CardContent>
          <h2 className="text-xl font-bold text-center mb-4">Insurance Finder</h2>
          <form onSubmit={handleSubmit} className="space-y-3">
            <Input name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
            <Input type="number" name="age" placeholder="Age" value={formData.age} onChange={handleChange} required />
            <Input type="date" name="dob" placeholder="Date of Birth" value={formData.dob} onChange={handleChange} required />
            <Input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
            <Input type="tel" name="phone" placeholder="Phone Number" value={formData.phone} onChange={handleChange} required />
            <Button type="submit" className="w-full">Find Insurance</Button>
          </form>
          {formData.insuranceType && (
            <p className="mt-4 text-center font-semibold text-blue-600">
              Recommended: {formData.insuranceType}
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}